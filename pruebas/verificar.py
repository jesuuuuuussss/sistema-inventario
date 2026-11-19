import argparse
import json
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

PRODUCTO = {
    "codigo": "PR7-001",
    "nombre": "Teclado USB",
    "precio": "249.90",
    "cantidad_disponible": 5,
    "categoria": "Accesorios",
}
DATOS_ESPERADOS = {k: v for k, v in PRODUCTO.items() if k != "precio"}
DATOS_ESPERADOS["precio_centavos"] = 24990


def solicitar(base, ruta, datos=None):
    if datos is None:
        request = Request(base + ruta)
    else:
        request = Request(
            base + ruta, data=json.dumps(datos).encode("utf-8"),
            headers={"Content-Type": "application/json"}, method="POST",
        )
    with urlopen(request, timeout=3) as respuesta:
        return respuesta.status, json.load(respuesta)


def comprobar_datos(producto):
    coincidencias = {campo: producto[campo] for campo in DATOS_ESPERADOS}
    if coincidencias != DATOS_ESPERADOS:
        raise RuntimeError(f"Datos de inventario diferentes a lo esperado: {coincidencias}")
    print(json.dumps(coincidencias, ensure_ascii=False), flush=True)


def esperar(base):
    limite = time.monotonic() + 15
    while True:
        try:
            return solicitar(base, "/health")
        except (URLError, TimeoutError):
            if time.monotonic() >= limite:
                raise
            time.sleep(0.25)


def main():
    parser = argparse.ArgumentParser(description="Verificar el Sistema de Inventario")
    parser.add_argument("--url", default="http://127.0.0.1:8000")
    parser.add_argument("--version", required=True)
    parser.add_argument("--accion", choices=("registrar", "consultar"), required=True)
    parser.add_argument("--consulta", default=PRODUCTO["codigo"])
    args = parser.parse_args()
    estado, salud = esperar(args.url)
    if estado != 200 or salud != {"estado": "ok", "version": args.version}:
        raise RuntimeError(f"Versión o estado no esperado: {salud}")
    print(f"GET /health → HTTP {estado}, versión {args.version}", flush=True)

    if args.accion == "registrar":
        estado, creado = solicitar(args.url, "/api/productos", PRODUCTO)
        if estado != 201:
            raise RuntimeError(f"Respuesta de alta no esperada: {estado}")
        print(f"POST /api/productos → HTTP {estado}, alta de {creado['codigo']}", flush=True)
        try:
            solicitar(args.url, "/api/productos", dict(PRODUCTO, codigo=" pr7-001 "))
        except HTTPError as error:
            if error.code != 400 or "Ya existe" not in json.load(error).get("error", ""):
                raise
        else:
            raise RuntimeError("Se aceptó un código duplicado.")
        print("Código duplicado → HTTP 400, rechazado", flush=True)

    ruta = "/api/productos?q=" + quote(args.consulta)
    estado, consulta = solicitar(args.url, ruta)
    if estado != 200 or len(consulta["productos"]) != 1:
        raise RuntimeError(f"Consulta no coincide con lo esperado: {consulta}")
    print(f"GET {ruta} → HTTP {estado}, 1 producto", flush=True)
    comprobar_datos(consulta["productos"][0])


if __name__ == "__main__":
    main()
