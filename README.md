# Sistema de inventario

Sistema web para la gestión de inventarios de un comercio electrónico.

Este repositorio reúne las prácticas 1, 2 y 3 de GitHub Projects: organización de un tablero Kanban, creación y seguimiento de Issues, configuración de campos personalizados y análisis del flujo DevOps. El trabajo entregado corresponde a la planificación y documentación del sistema.

- **Cuenta:** [jesuuuuuussss](https://github.com/jesuuuuuussss).
- **Proyecto:** DevOps - Sistema de Inventario.
- **[Abrir la vista Board](https://github.com/users/jesuuuuuussss/projects/1/views/2)**.
- **[Consultar las Issues](https://github.com/jesuuuuuussss/sistema-inventario/issues?q=is%3Aissue)**.
- **[Estructura de productos](docs/estructura-productos.md)**.
- **[Capturas de evidencia](docs/evidencias/)**.

El repositorio es público e incluye `README.md`, `.gitignore` para Node y licencia MIT. La plantilla de exclusión prepara un posible desarrollo web; estas prácticas no incluyen una aplicación ejecutable.

## Práctica 1 Tablero Kanban

La vista **Board** está agrupada por **Status**, con las columnas en este orden:

| Orden | Columna | Significado |
| --- | --- | --- |
| 1 | Backlog | Ideas y necesidades pendientes de preparar o priorizar. |
| 2 | Por hacer | Tareas definidas y listas para comenzar. |
| 3 | En progreso | Tareas que se están realizando. |
| 4 | En revisión | Tareas que requieren validación. |
| 5 | Terminado | Tareas que cumplieron sus criterios de aceptación. |

La vista usa el filtro `repo:jesuuuuuussss/sistema-inventario` para consultar las 11 Issues de esta práctica. El proyecto ya existía y se completó mediante esta vista específica.

### Análisis del tablero

**¿Por qué un equipo de desarrollo necesita visualizar el estado de sus tareas?**  
Para conocer qué está pendiente, quién necesita apoyo y dónde se acumula el trabajo. La visualización permite coordinar el esfuerzo y detectar bloqueos antes de que retrasen una entrega.

**¿Qué diferencia existe entre Backlog y Por hacer?**  
Backlog contiene necesidades que todavía pueden requerir análisis, prioridad o definición. Por hacer reúne las tareas que ya tienen un alcance claro, criterios de aceptación y condiciones para comenzar.

**¿Cuándo una tarea debe pasar de Por hacer a En progreso?**  
Cuando alguien comienza a trabajar en ella, conoce el resultado esperado y dispone de lo necesario para avanzar. El cambio debe reflejar el trabajo real, evitando abrir más tareas de las que se pueden atender.

**¿Por qué una tarea no debería pasar directamente de En progreso a Terminado?**  
Porque terminar de elaborar o programar algo no demuestra por sí mismo que sea correcto. Antes de finalizar, se deben revisar el resultado, las validaciones y los criterios de aceptación; en tareas de código también se necesitan las pruebas pertinentes.

**¿Qué función cumple la columna En revisión?**  
Hace visible el trabajo pendiente de comprobar. Sirve para revisar diseño o código, ejecutar pruebas, confirmar requisitos y solicitar correcciones antes de aceptar una tarea.

**¿Qué relación tiene este tablero con la entrega continua en DevOps?**  
Permite seguir el avance de cambios pequeños y detectar esperas entre desarrollo, revisión y validación. Complementa las pruebas y la automatización de integración y entrega. El tablero por sí solo no construye ni despliega software.

## Práctica 2 Repositorio e Issues

Se crearon las diez Issues indicadas en el documento y una adicional para el reto de la práctica 3. Cada Issue incluye descripción, actividades y criterios de aceptación.

La distribución inicial fue:

- **Backlog:** #5, #6, #7, #8, #9 y #10.
- **Por hacer:** #1, #2, #3 y #4.
- **En progreso, En revisión y Terminado:** inicialmente vacías.

El documento especifica el estado inicial de ocho tareas. Las Issues #5 y #7 se ubicaron en Backlog porque todavía requieren preparación antes de iniciar. La Issue #11 se agregó después, también a Backlog.

### Simulación del flujo

La Issue [#1 Diseñar estructura de productos](https://github.com/jesuuuuuussss/sistema-inventario/issues/1) recorrió:

**Por hacer → En progreso → En revisión → Terminado**

Su entregable es [la propuesta de estructura de productos](docs/estructura-productos.md), que define nombre, código, precio, cantidad disponible y categoría, además de tipos y reglas de validación. La Issue quedó cerrada como completada después de documentar y revisar la propuesta.

## Práctica 3 Campos personalizados

Los tres campos son de tipo **Single select**:

| Campo | Opciones |
| --- | --- |
| Prioridad | Alta, Media, Baja |
| Fase DevOps | PLAN, CODE, BUILD, TEST, RELEASE, DEPLOY, OPERATE, MONITOR |
| Estimación | 1, 2, 3, 5, 8 |

### Significado de las fases

| Fase | Significado |
| --- | --- |
| PLAN | Planificación del trabajo. |
| CODE | Desarrollo del código. |
| BUILD | Construcción del software. |
| TEST | Pruebas y validación. |
| RELEASE | Preparación de la versión. |
| DEPLOY | Despliegue. |
| OPERATE | Operación del sistema. |
| MONITOR | Monitoreo. |

Una actividad puede relacionarse con varias fases durante su ciclo de vida. El campo indica la fase que representa principalmente su propósito actual.

### Escala de estimación

| Estimación | Interpretación |
| --- | --- |
| 1 | Muy pequeña. |
| 2 | Pequeña. |
| 3 | Moderada. |
| 5 | Grande. |
| 8 | Muy grande. |

Los valores representan esfuerzo o complejidad relativos. No equivalen directamente a horas.

### Configuración final de las Issues

| Issue | Tarea | Estado | Prioridad | Fase DevOps | Estimación |
| --- | --- | --- | --- | --- | --- |
| [#1](https://github.com/jesuuuuuussss/sistema-inventario/issues/1) | Diseñar estructura de productos | Terminado | Alta | PLAN | 3 |
| [#2](https://github.com/jesuuuuuussss/sistema-inventario/issues/2) | Diseñar formulario de registro de productos | Por hacer | Alta | PLAN | 5 |
| [#3](https://github.com/jesuuuuuussss/sistema-inventario/issues/3) | Implementar registro de productos | En revisión | Alta | TEST | 5 |
| [#4](https://github.com/jesuuuuuussss/sistema-inventario/issues/4) | Implementar consulta de productos | Por hacer | Media | CODE | 3 |
| [#5](https://github.com/jesuuuuuussss/sistema-inventario/issues/5) | Implementar modificación de productos | Backlog | Media | CODE | 5 |
| [#6](https://github.com/jesuuuuuussss/sistema-inventario/issues/6) | Implementar eliminación de productos | Backlog | Media | CODE | 3 |
| [#7](https://github.com/jesuuuuuussss/sistema-inventario/issues/7) | Implementar búsqueda de productos | Backlog | Media | CODE | 3 |
| [#8](https://github.com/jesuuuuuussss/sistema-inventario/issues/8) | Implementar control de existencias | Backlog | Alta | CODE | 8 |
| [#9](https://github.com/jesuuuuuussss/sistema-inventario/issues/9) | Diseñar módulo de usuarios | Backlog | Alta | PLAN | 5 |
| [#10](https://github.com/jesuuuuuussss/sistema-inventario/issues/10) | Diseñar reporte de inventario | Backlog | Baja | PLAN | 3 |
| [#11](https://github.com/jesuuuuuussss/sistema-inventario/issues/11) | Mejorar búsqueda de productos | Backlog | Alta | CODE | 5 |

La Issue #3 se configuró primero en CODE, como indica el ejemplo, y después pasó a TEST para resolver la situación B. El estado final del tablero es: 7 tareas en Backlog, 2 en Por hacer, 0 en En progreso, 1 en En revisión y 1 en Terminado.

### Situación A Registrar productos antes de la revisión

**Issue que debe recibir mayor atención:** #3 Implementar registro de productos.  
**Prioridad:** Alta.  
**Estimación:** 5.  
**Fase principal en el momento de programarla:** CODE.

El registro es necesario para empezar a utilizar el inventario y el cliente lo necesita antes de la próxima revisión. La estimación 5 considera las validaciones, la prevención de duplicados, la persistencia y el manejo de errores. Antes de desarrollarlo se necesitan la estructura de productos y el diseño del formulario. La urgencia no elimina las pruebas ni justifica reducir la estimación.

### Situación B La programación terminó y se debe comprobar el registro

La Issue #3 se movió de Por hacer a En progreso, cambió su fase principal de **CODE a TEST** y quedó en **En revisión**, conservando prioridad Alta y estimación 5.

Ahora el propósito principal es comprobar que el registro funciona: altas válidas, campos obligatorios, códigos duplicados, precios o cantidades inválidos y disponibilidad del producto en la consulta. Aunque la tarea mantiene relación con CODE por su desarrollo previo, TEST describe mejor la actividad actual. Si aparecen fallos, deberá regresar a desarrollo para corregirse.

Este cambio representa la simulación académica solicitada. No afirma que en estas prácticas ya se haya programado o probado una aplicación.

### Reto Mejorar búsqueda de productos

Se creó la Issue [#11 Mejorar búsqueda de productos](https://github.com/jesuuuuuussss/sistema-inventario/issues/11) con el requisito: **buscar productos por nombre, código y categoría**.

- **Prioridad Alta:** responde a una necesidad explícita del cliente que facilita localizar productos. Se atenderá después de contar con registro y consulta básicos.
- **Fase CODE:** el requisito ya está expresado y el trabajo principal consiste en ampliar la lógica y los filtros de búsqueda.
- **Estimación 5:** integrar tres criterios, definir combinaciones y validar casos distintos requiere más esfuerzo que la búsqueda básica estimada en 3.

La mejora amplía el alcance de la Issue #7. Se mantiene en Backlog hasta preparar sus dependencias y comenzar su ejecución.

### Reflexión

**¿Qué problema resuelve el campo Prioridad?**  
Ayuda a decidir qué tareas atender primero según su valor, urgencia y dependencias.

**¿Para qué sirve identificar la Fase DevOps?**  
Permite distinguir el propósito actual de cada tarea y coordinar planificación, desarrollo, pruebas y operación. La fase puede actualizarse cuando cambia el tipo de trabajo.

**¿Por qué la estimación no representa necesariamente horas de trabajo?**  
Porque compara dificultad, volumen e incertidumbre de las tareas. El tiempo real depende también de la experiencia, las herramientas, las interrupciones y las dependencias.

**¿Qué puede ocurrir si todas las tareas tienen prioridad Alta?**  
La prioridad deja de ayudar a decidir. Se pueden repartir esfuerzos en demasiadas actividades y retrasar los resultados que el cliente necesita primero.

**¿Por qué es importante estimar antes de comenzar a desarrollar?**  
Para detectar tareas grandes o poco claras, conversar sobre dependencias y comprometer una cantidad de trabajo razonable. Una estimación también ayuda a decidir cuándo dividir una tarea.

**¿Qué información adicional proporciona ahora el tablero respecto a la práctica anterior?**  
Además del estado, muestra la importancia de cada Issue, su fase principal y el esfuerzo relativo previsto. Esto facilita priorizar y explicar la carga de trabajo.

## Evidencias

Las capturas se conservan en [docs/evidencias](docs/evidencias/):

1. **Campos personalizados:** `github-inventario-campos.jpg`, con Prioridad, Fase DevOps y Estimación visibles en Settings.
2. **Board:** capturas de las secciones izquierda y derecha, con las cinco columnas en orden y los campos de las Issues.
3. **Nueva Issue:** `github-inventario-mejora-busqueda.jpg`, con los campos configurados para el reto.

## Licencia

Este repositorio se distribuye bajo la [licencia MIT](LICENSE).
