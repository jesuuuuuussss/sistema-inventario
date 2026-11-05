# Estructura de productos

Propuesta de datos para el Sistema de Inventario. Esta definición resuelve la Issue #1 y sirve como base para el formulario, el registro, la consulta y el control de existencias.

## Datos del producto

| Campo | Tipo propuesto | Obligatorio | Regla |
| --- | --- | --- | --- |
| id | UUID | Sí, generado | Identificador interno único e inmutable. |
| nombre | Texto de hasta 150 caracteres | Sí | Eliminar espacios al inicio y final; no aceptar texto vacío. |
| codigo | Texto de hasta 50 caracteres | Sí | Código comercial único; normalizar espacios y mayúsculas antes de comprobar duplicados. Conservarlo como texto para respetar ceros iniciales. |
| precio | Decimal de 12 dígitos y 2 decimales | Sí | Importe en MXN mayor o igual a cero; usar decimal y no punto flotante binario. |
| cantidad_disponible | Entero | Sí | Unidades disponibles mayores o iguales a cero; valor inicial 0 si no se indica otra cantidad válida. |
| categoria_id | UUID | Sí | Referencia a una categoría existente. |
| descripcion | Texto de hasta 1000 caracteres | No | Información complementaria del producto. |
| activo | Booleano | Sí, generado | Valor inicial verdadero; permite dar de baja productos con historial. |
| creado_en | Fecha y hora con zona horaria | Sí, generado | Momento de creación del registro. |
| actualizado_en | Fecha y hora con zona horaria | Sí, generado | Momento de la última modificación. |

## Categorías

Cada categoría tendrá `id`, `nombre` y `activo`. El nombre será obligatorio y único, sin distinguir mayúsculas y minúsculas. Una categoría puede contener varios productos; cada producto pertenecerá a una categoría en esta primera propuesta. Las categorías con productos asociados se desactivarán en lugar de eliminarse sin validación.

## Reglas de validación y existencias

1. Nombre, código, precio y categoría son obligatorios. La cantidad debe ser un número entero mayor o igual a cero.
2. Se debe garantizar la unicidad del código tanto en la validación de la aplicación como mediante una restricción del almacenamiento.
3. El precio se validará con un máximo de dos decimales y dentro del rango del tipo propuesto. La moneda inicial del sistema será MXN.
4. Esta propuesta administra productos por unidades enteras; los productos vendidos por peso requerirían una ampliación del modelo.
5. Después del alta, las existencias se modificarán mediante movimientos de entrada, salida o ajuste, conservando cantidad, tipo, motivo, producto, fecha y responsable.
6. La actualización de existencias y su movimiento deben ejecutarse de forma atómica para evitar saldos inconsistentes; ninguna salida podrá producir existencias negativas.
7. Los productos con movimientos históricos se darán de baja mediante `activo`, conservando la trazabilidad.

## Ejemplo de producto válido

```json
{
  "nombre": "Teclado USB",
  "codigo": "TEC-0001",
  "precio": "249.90",
  "cantidad_disponible": 20,
  "categoria": "Accesorios",
  "descripcion": "Teclado alámbrico en español"
}
```

El identificador de categoría se resolverá contra el catálogo existente; el ejemplo usa el nombre para facilitar la lectura. El identificador del producto y las fechas se generarán al registrar.

## Validación de la propuesta

La definición incluye nombre, código, precio, cantidad disponible y categoría, como solicita la práctica. Precisa tipos, obligatoriedad y reglas; prevé unicidad, integridad y trazabilidad. Es una propuesta de diseño: no supone que la aplicación o la base de datos ya estén implementadas.
