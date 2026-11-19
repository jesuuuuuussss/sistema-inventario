from __future__ import annotations

import re
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from uuid import NAMESPACE_URL, uuid4, uuid5

CATEGORIAS = ("Accesorios", "Electrónica", "Hogar", "Papelería", "Otro")


def formatear_precio(centavos):
    return "$" + f"{centavos // 100:,}.{centavos % 100:02d}"


def texto_obligatorio(datos, campo, limite, etiqueta):
    valor = datos.get(campo, "")
    if not isinstance(valor, str) or not 0 < len(valor.strip()) <= limite:
        raise ValueError(f"{etiqueta} es obligatorio y admite hasta {limite} caracteres.")
    return valor.strip()


class Inventario:
    def __init__(self, ruta):
        self.ruta = ruta

    def conectar(self):
        con = sqlite3.connect(self.ruta)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA foreign_keys=ON")
        return con

    def preparar(self):
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        with closing(self.conectar()) as con, con:
            con.executescript("""
                CREATE TABLE IF NOT EXISTS categorias (
                    id TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL UNIQUE,
                    activo INTEGER NOT NULL DEFAULT 1
                );
                CREATE TABLE IF NOT EXISTS productos (
                    id TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    codigo TEXT NOT NULL UNIQUE,
                    precio_centavos INTEGER NOT NULL CHECK (precio_centavos >= 0),
                    cantidad_disponible INTEGER NOT NULL CHECK (cantidad_disponible >= 0),
                    categoria_id TEXT NOT NULL REFERENCES categorias(id),
                    descripcion TEXT NOT NULL DEFAULT '',
                    activo INTEGER NOT NULL DEFAULT 1,
                    creado_en TEXT NOT NULL,
                    actualizado_en TEXT NOT NULL
                );
            """)
            con.executemany(
                "INSERT OR IGNORE INTO categorias(id, nombre) VALUES (?, ?)",
                [(str(uuid5(NAMESPACE_URL, "inventario:categoria:" + nombre)), nombre)
                 for nombre in CATEGORIAS],
            )

    def consultar(self, filtro=""):
        query = """
            SELECT p.id, p.codigo, p.nombre, p.precio_centavos, p.cantidad_disponible,
                   p.descripcion, c.nombre AS categoria
            FROM productos p JOIN categorias c ON c.id = p.categoria_id
            WHERE p.activo = 1 AND (? = '' OR p.codigo = ?)
            ORDER BY p.codigo
        """
        codigo = " ".join(filtro.split()).upper()
        with closing(self.conectar()) as con:
            return [dict(fila) for fila in con.execute(query, (codigo, codigo))]

    def registrar(self, datos):
        nombre = texto_obligatorio(datos, "nombre", 150, "El nombre")
        codigo = " ".join(texto_obligatorio(datos, "codigo", 50, "El código").split()).upper()
        if len(codigo) > 50:
            raise ValueError("El código admite hasta 50 caracteres.")
        importe = str(datos.get("precio", "")).strip()
        if not re.fullmatch(r"[0-9]{1,10}(?:\.[0-9]{1,2})?", importe):
            raise ValueError("Escribe un precio en MXN con hasta dos decimales.")
        entero, _, decimal = importe.partition(".")
        centavos = int(entero) * 100 + int(decimal.ljust(2, "0"))
        cantidad = str(datos.get("cantidad_disponible", "")).strip() or "0"
        if not re.fullmatch(r"[0-9]{1,19}", cantidad) or int(cantidad) > 2**63 - 1:
            raise ValueError("La cantidad debe ser un entero mayor o igual a cero.")
        categoria = datos.get("categoria")
        if categoria not in CATEGORIAS:
            raise ValueError("Selecciona una categoría del catálogo.")
        descripcion = datos.get("descripcion", "")
        if not isinstance(descripcion, str) or len(descripcion.strip()) > 1000:
            raise ValueError("La descripción admite hasta 1000 caracteres.")

        producto = {
            "id": str(uuid4()),
            "codigo": codigo,
            "nombre": nombre,
            "precio_centavos": centavos,
            "cantidad_disponible": int(cantidad),
            "categoria": categoria,
            "descripcion": descripcion.strip(),
        }
        ahora = datetime.now(timezone.utc).isoformat(timespec="seconds")
        with closing(self.conectar()) as con, con:
            categoria_id = con.execute(
                "SELECT id FROM categorias WHERE nombre = ? AND activo = 1", (categoria,)
            ).fetchone()
            if categoria_id is None:
                raise ValueError("La categoría no está disponible.")
            try:
                con.execute("""
                    INSERT INTO productos(
                        id, nombre, codigo, precio_centavos, cantidad_disponible,
                        categoria_id, descripcion, creado_en, actualizado_en
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    producto["id"], nombre, codigo, centavos, int(cantidad),
                    categoria_id["id"], descripcion.strip(), ahora, ahora,
                ))
            except sqlite3.IntegrityError as error:
                if error.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
                    raise ValueError("Ya existe un producto con ese código.") from error
                raise
        return producto
