from __future__ import annotations

import argparse
import html
import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlsplit

from almacen import CATEGORIAS, Inventario, formatear_precio

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
TEMPLATE = (ROOT / "src" / "vista.html").read_text(encoding="utf-8")
CSS = (ROOT / "src" / "estilos.css").read_bytes()


def texto(valor):
    return html.escape(str(valor), quote=True)


def tabla(productos):
    if not productos:
        return '<tr><td colspan="5" class="vacio">No hay productos para mostrar.</td></tr>'
    filas = []
    for producto in productos:
        filas.append(
            "<tr>"
            f'<td class="codigo">{texto(producto["codigo"])}</td>'
            f'<td>{texto(producto["nombre"])}</td>'
            f'<td>{texto(producto["categoria"])}</td>'
            f'<td class="numero">{formatear_precio(producto["precio_centavos"])}</td>'
            f'<td class="numero">{producto["cantidad_disponible"]}</td>'
            "</tr>"
        )
    return "\n".join(filas)


class Aplicacion(BaseHTTPRequestHandler):
    server_version = "Inventario"
    sys_version = ""

    def responder(self, estado, contenido, tipo):
        self.send_response(estado)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(contenido)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(contenido)

    def json(self, estado, datos):
        cuerpo = json.dumps(datos, ensure_ascii=False).encode("utf-8")
        self.responder(estado, cuerpo, "application/json; charset=utf-8")

    def vista(self, *, consulta="", mensaje="", error=False, datos=None):
        datos = datos or {}
        opciones = "".join(
            f'<option value="{texto(nombre)}"{" selected" if datos.get("categoria") == nombre else ""}>'
            f"{texto(nombre)}</option>"
            for nombre in CATEGORIAS
        )
        clase = "error" if error else "confirmacion"
        aviso = f'<p role="status" class="aviso {clase}">{texto(mensaje)}</p>' if mensaje else ""
        campos = {
            "version": texto(VERSION),
            "mensaje": aviso,
            "consulta": texto(consulta),
            "filas": tabla(self.server.inventario.consultar(consulta)),
            "opciones": opciones,
        }
        for campo in ("nombre", "codigo", "precio", "cantidad_disponible"):
            campos[campo] = texto(datos.get(campo, ""))
        cuerpo = TEMPLATE.format_map(campos).encode("utf-8")
        estado = HTTPStatus.BAD_REQUEST if error else HTTPStatus.OK
        self.responder(estado, cuerpo, "text/html; charset=utf-8")

    def do_GET(self):
        url = urlsplit(self.path)
        args = parse_qs(url.query)
        consulta = args.get("q", [""])[0].strip()[:150]
        if url.path == "/":
            creado = args.get("creado", [""])[0][:50]
            mensaje = f"Producto {creado} registrado correctamente." if creado else ""
            self.vista(consulta=consulta, mensaje=mensaje)
        elif url.path == "/estilos.css":
            self.responder(HTTPStatus.OK, CSS, "text/css; charset=utf-8")
        elif url.path == "/health":
            self.json(HTTPStatus.OK, {"estado": "ok", "version": VERSION})
        elif url.path == "/api/productos":
            self.json(HTTPStatus.OK, {
                "version": VERSION, "productos": self.server.inventario.consultar(consulta)
            })
        else:
            self.json(HTTPStatus.NOT_FOUND, {"error": "Ruta no encontrada."})

    def do_POST(self):
        if self.path not in ("/productos", "/api/productos"):
            self.json(HTTPStatus.NOT_FOUND, {"error": "Ruta no encontrada."})
            return
        api = self.path == "/api/productos"
        datos = {}
        try:
            tamano = int(self.headers.get("Content-Length", "0"))
            if not 0 < tamano <= 8192:
                raise ValueError("Solicitud vacía o demasiado grande.")
            cuerpo = self.rfile.read(tamano).decode("utf-8")
            if api:
                datos = json.loads(cuerpo)
                if not isinstance(datos, dict):
                    datos = {}
                    raise ValueError("Se esperaba un objeto de producto.")
            else:
                datos = {campo: valores[0] for campo, valores in
                         parse_qs(cuerpo, keep_blank_values=True).items()}
            producto = self.server.inventario.registrar(datos)
        except ValueError as error:
            if api:
                self.json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
            else:
                self.vista(mensaje=str(error), error=True, datos=datos)
            return

        if api:
            self.json(HTTPStatus.CREATED, producto)
        else:
            query = urlencode({"creado": producto["codigo"]})
            self.send_response(HTTPStatus.SEE_OTHER)
            self.send_header("Location", "/?" + query)
            self.send_header("Content-Length", "0")
            self.end_headers()


def main():
    parser = argparse.ArgumentParser(description="Sistema de Inventario")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--db", type=Path,
                        default=Path(os.environ.get("INVENTARIO_DB", "datos/inventario.sqlite3")))
    args = parser.parse_args()
    inventario = Inventario(args.db)
    inventario.preparar()
    with ThreadingHTTPServer((args.host, args.port), Aplicacion) as server:
        server.inventario = inventario
        print(f"Inventario {VERSION} en http://{args.host}:{server.server_port}", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
