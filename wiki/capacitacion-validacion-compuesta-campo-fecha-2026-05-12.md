---
type: Fuente de video
title: "Capacitación: validación compuesta – campo fecha (12/05/2026)"
description: Cómo manejar un filtro de fecha compuesto (fecha desde/hasta) en una pantalla migrada desde Forms. Cubre campos auxiliares, la lectura del JSON en el type, el validador de fechas y el problema de rendimiento cuando la fecha tiene hora (TRUNC frente a ">= desde y < hasta + 1").
resource: "Transcripciones/Tecnaris - Modernización de módulos-20260512_Capacitacion validacion compuesta.docx"
timestamp: 2026-05-12
duracion: "0:46:00"
participantes: []
dominio: tecnico
tags: [modernizacion-de-modulos, oracle-forms, migracion, valor-compuesto, campo-fecha, operatoria, filtro, validador, json, type, rectype, campo-query, performance, indices, trunc, case-restriction, titulos]
estado: borrador
calidad_transcripcion: baja
---

# Capacitación: validación compuesta – campo fecha (12/05/2026)

## Resumen

- Caso trabajado: una pantalla de **log** (tabla con prefijo "Q" [?], form "51736"/"517366" [?]) cuyo filtro en Forms usa **fecha desde / fecha hasta sobre un mismo campo**.
- El Front se comunica con el back mediante un **JSON** con nombre de campo y valor. Un transformador lo vuelca al **type** generado, que usa los mismos nombres de campo. Cuando el valor es **compuesto** (numérico o fecha), el Front manda **dos valores** con un formato especial que genera solo.
- En la **operatoria** se define el campo fecha como **compuesto** y se copia el WHERE del bloque del Forms al **filtro**, salvo la parte de fechas: esa la arma el Front (fecha entre desde y hasta).
- El back usa las dos fechas **solo para validar**. Para eso se agregan **campos auxiliares** (fecha desde / fecha hasta) en la definición. En la asignación JSON → type se llama al procedimiento de plantilla **"obtener valores del JSON fecha"**.
- No se llama a ese procedimiento en todos los campos fecha, por rendimiento: en el ~95 % de los casos no son compuestos.
- El **validador** recibe el rectype (un registro ya cargado desde el JSON) y el usuario, y devuelve error. Valida que ambas fechas estén cargadas, que desde ≤ hasta y que no haya más de **30 días** entre ellas. Siempre corta con **RETURN** después de un error.
- Si un validador además **modifica otros campos**, debe ejecutar la línea final que reasigna los valores modificados al JSON y los devuelve.
- Tipos de validación de filtro en la parametrización: **valida** (una sola fecha), **valida compuesto** (dos fechas, requiere programar el type) y **no valida** (dos fechas sin validar, no hay que tocar el type).
- **Problema de la hora**: la fecha guardada tiene hora y el Forms filtra con TRUNC, que rompe el índice. Lo correcto, con índice por fecha, es **fecha >= desde AND fecha < hasta + 1**. La solución provisoria: devolver TRUNC(fecha) en el select y marcar el campo como **no parte del query**, de modo que el Front filtre después de traer los datos (menos performante).
- Correcciones pendientes de la definición: **Case Restriction** según el tipo (NUMBER/MONTO, MIXED/UPPER…, DATE) y **títulos** de todos los campos como se ven en el Forms.

## Temas

| # | Tema | Desde | Hasta | Dominio |
|---|---|---|---|---|
| 1 | Valores compuestos: JSON del Front, type y campos auxiliares | 0:02 | 3:59 | tecnico |
| 2 | Análisis del Forms: WHERE del bloque y operatoria con fecha compuesta | 6:51 | 10:42 | tecnico |
| 3 | Asignación JSON → type: "obtener valores del JSON fecha" | 10:42 | 18:32 | tecnico |
| 4 | Validador de fecha: formato, RETURN y reglas | 18:32 | 24:43 | tecnico |
| 5 | Validadores que modifican otros campos | 24:43 | 28:00 | tecnico |
| 6 | Parametrización del filtro: valida, valida compuesto y no valida | 28:00 | 29:54 | tecnico |
| 7 | Fecha con hora: TRUNC, índices y campo fuera del query | 29:54 | 41:13 | tecnico |
| 8 | Marcar el campo como no query, Case Restriction, títulos y tarea | 41:13 | 45:06 | tecnico |

## Transcripción limpia por tema

### 1. Valores compuestos: JSON del Front, type y campos auxiliares (0:02 – 3:59)

[0:02] Para el caso "51736" [?] hay que arrancar generando **campos auxiliares de consulta**. Después se van a usar funciones predeterminadas: el JSON viene en un formato conocido, con dos fechas. [0:29] Se llama a un procedimiento predefinido que devuelve **fecha desde y fecha hasta**, y esos valores hay que guardarlos en algún campo para después validarlos. Eso se hace del lado del **type**, al definirlo.

[0:56] Repaso de la comunicación con el Front: el Front manda un **JSON con el nombre de cada campo y su dato**. En el medio hay un **transformador** que lo convierte al type que definimos; se puede porque el type generado usa los mismos nombres de campo.

[1:25] Con los **valores compuestos**, tanto numéricos como de fecha, la cosa cambia: ya no viene un solo valor sino **dos**, con un formato especial que el **Front genera automáticamente**. [1:56] El form de referencia se dicta como "CBKF 517366" [?].

[2:14] Al armar el type, uno de los participantes ya había creado dos campos previendo esto: sabía que iba a recibir un string con las dos fechas y que debía cargarlo en el paquete para agregar sus validaciones, pero no conocía el procedimiento de conversión. [2:14] La tabla es "queue punto Log" [?]. [3:23] Prefijo: "cu" (Q) [?]. [2:50] Se trabaja en desa ("actualizaciones … de desa").

[3:59] Al generar el script se van a mostrar las funciones que queden en la plantilla; mientras tanto queda la grabación.

### 2. Análisis del Forms: WHERE del bloque y operatoria con fecha compuesta (6:51 – 10:42)

[6:51] Primero hay que analizar el Forms. En el bloque del log se ve qué tabla usa y que tiene un **WHERE**.

> **Regla:** [6:51–7:17] El WHERE del bloque del Forms se pasa al **filtro de la operatoria**. La parte de las fechas no se copia, porque llega por parámetro y se parametriza en la operatoria.

[7:43] La operatoria del Forms tiene **fecha desde y fecha hasta sobre un mismo campo**. Por eso, al definir la operatoria, se indica que el campo "fecha" es **compuesto**: así se sabe que llegan dos valores para ese mismo campo, aunque en la tabla haya una sola fecha.

[8:13] En la definición ya están los campos de la tabla (ID, usuario, IP, fecha). No conviene agregar "fecha desde/fecha hasta" como campos comunes: la fecha desde ya viene como parámetro.

[9:13] Al marcar el campo fecha como compuesto en la parametrización, el Front muestra **dos fechas** y nos pasa los datos **para validarlos**, pero después no hace nada más con ellas en el back. Es el **Front el que arma** el "fecha entre desde y hasta".

> **Regla:** [9:41] Los campos auxiliares de fecha desde/hasta solo hacen falta si hay que **validar** el rango. El back no filtra ni arma ningún WHERE con ellos; eso lo hace el Front.

[10:16] Validaciones del Forms original: que existan las dos fechas, que la primera sea menor que la segunda (al revés da error) y que **no haya más de 30 días** entre ambas. Por lo tanto, en este caso sí hay que validar.

### 3. Asignación JSON → type: "obtener valores del JSON fecha" (10:42 – 18:32)

[10:42] Los campos auxiliares definidos pueden quedar en nulo, y está bien. [11:09] Hasta acá se hizo todo bien: están todos los campos de la tabla y se agregaron dos campos auxiliares de fecha. Con los numéricos compuestos se hace exactamente lo mismo.

[11:48] En el type ("Q… LOG rectype" [?]) hay un procedimiento que construye el registro a partir del JSON. [12:13] Si llega el dato de un campo, lo asigna a **un solo campo del registro**. El problema es que para la fecha compuesta llegan dos valores.

[12:38] Para eso hay plantillas de dos procedimientos. Para fechas se usa **"obtener valores del JSON fecha"**. [13:11] Si llega el campo fecha y se lo definió como compuesto en la parametría, se llama a ese procedimiento; si no es compuesto, no pasa nada. La plantilla va a quedar incluida.

[13:44] Qué recibe: el **JSON**, el **formato de fecha** (está definido; puede incluir formato de hora) y el valor del campo. [14:26] Si se usa el formato de fecha por defecto, alcanza. Qué devuelve:

- si el campo no es compuesto, el mismo valor único de antes (valor fecha out);
- si es compuesto, la **fecha desde** y la **fecha hasta**.

[14:57] En el ejemplo, la primera fecha se carga en el campo fecha, y fecha desde / fecha hasta en los auxiliares.

> **Caso especial:** [15:23–17:58] Se podría llamar a la función para **todo** campo fecha, pero en el ~95 % de los casos no son compuestos y se la llamaría muchas veces sin necesidad. Además, cada campo fecha necesitaría su par desde/hasta: con 5 fechas en una tabla serían 15 campos solo para carga. Por **rendimiento** se llama solo en el campo definido como compuesto.

[17:03] Los campos desde/hasta se cargan **con el único objetivo de validar**. Con los numéricos compuestos ("combinados") se procede igual. [17:58] Una vez cargados, lo que sigue va en el procedimiento de validación.

### 4. Validador de fecha: formato, RETURN y reglas (18:32 – 24:43)

[18:32] En el paquete hay un procedimiento **"validar operatoria de filtro"**, que valida las operatorias y los filtros definidos. Ahí ya están cargados el campo fecha y los auxiliares, así que solo queda validarlos con un **"validar fecha"**.

[19:58] Formato de un validador nuevo:

- recibe el **rectype**, que es un solo registro ya cargado desde el JSON;
- recibe el **usuario**, por si hace falta;
- devuelve si hay **error** o no.

> **Regla:** [19:58–20:26] Después de cargar un error, poner siempre **RETURN**. Si no, una mala programación puede seguir ejecutando lo que viene después y terminar "todo bien" cuando no lo está. Cada validador debe llevar el **nombre del campo** que valida.

[20:52] Si las validaciones son muy distintas, se pueden separar ("validar fecha 1", "validar fecha 2") o dejar todo en un solo procedimiento, discriminando por tipo.

[21:48] Al copiar la lógica del Forms, las referencias `:bloque.campo` se reemplazan por los campos del registro y por los auxiliares fecha desde / fecha hasta.

Reglas del validador para este caso:

- [22:41] **Si alguna de las dos fechas es nula** (OR), error *"Debe ingresar fecha desde y fecha hasta"* y RETURN. [23:11] Se cree que cuando se carga la primera, el Front copia el valor en la segunda [?].
- [24:18] Si fecha desde es mayor que fecha hasta, error.
- [24:18] Si hay más de 30 días entre las fechas, error.

[24:18] No hay que programar la ejecución del query posterior (equivalente al GO_BLOCK / EXECUTE_QUERY del Forms): la hace el validador automáticamente. Solo se programan las validaciones.

### 5. Validadores que modifican otros campos (24:43 – 28:00)

[24:43] Lo más importante del procedimiento es que recibe el rectype con el usuario y el dato. [25:09] A veces un validador no solo verifica la fecha: si llega un dato, puede tener que completar otro campo.

> **Regla:** [25:43–27:30] Si el validador **asigna o modifica otros campos** (por ejemplo, busca compañía, sucursal o agencia y los carga), tiene que ejecutar al final la línea que **reasigna los valores modificados al JSON y los devuelve**. Si solo valida, no hace falta. Con varios validadores, algunos que modifican y otros que no, hay que ubicar esa línea de forma que no se pierdan cambios.

[26:35] Para probarlo, asignar un valor a algún campo dentro del validador y verificar que vuelva.

### 6. Parametrización del filtro: valida, valida compuesto y no valida (28:00 – 29:54)

[28:00] En la parametrización, el campo fecha lleva un **validador compuesto**. [28:30] Se configura en la **operatoria**, en el filtro. Hay tres opciones:

| Opción | Qué muestra el Front | Qué hay que programar |
|---|---|---|
| **Valida** (normal) | una sola fecha | validar sobre ese único campo, sin campos adicionales |
| **Valida compuesto** | dos fechas | programar en el type dónde guardar la segunda fecha y validarlas |
| **No valida** | dos fechas | nada: no hay validación ni cambios en el type |

[29:29] Además, en la operatoria va el WHERE del bloque visto antes, sin la parte de la fecha.

### 7. Fecha con hora: TRUNC, índices y campo fuera del query (29:54 – 41:13)

[30:24] El Forms aplica **TRUNC** a la fecha porque el campo tiene hora. Con "fecha hasta" sin truncar no entran los registros con minutos y segundos de ese mismo día.

[31:21] El Front arma "fecha entre X e Y" y no sabe que la fecha tiene hora. [31:21–31:50] Lo correcto sería:

> **Regla:** [39:04–40:17] Con **índice por fecha**, filtrar con **fecha >= fecha_desde AND fecha < fecha_hasta + 1**. El "menor estricto que hasta + 1" incluye todo el último día hasta 23:59:59. Con "<= fecha hasta" solo entran los del día 5 a las 0:00; los de las 10, 11 o 12 horas quedan afuera. **TRUNC sobre la columna rompe el índice.**

[32:17–33:16] Alternativas para "engañar" al Front, que solo maneja un campo:

- concatenar la hora 00:00 en el select;
- crear otro campo ("fecha WHERE") que **no sea campo de la tabla**.

[33:46–35:13] Solución aplicada para este caso:

- en el **select**, devolver **TRUNC(fecha)** con el alias del campo fecha;
- marcar el campo fecha como **no parte del query**.

Así, la base filtra por todos los demás campos y el Front filtra por la fecha recién cuando recibe los datos.

> **Regla:** [35:13–35:42] Si un campo está marcado como parte del query, el filtro va al WHERE de la base. Si no lo está, se ejecuta el query con el resto de los filtros y el filtrado por ese campo se hace al recibir los datos. Esto es **poco performante**, por eso siempre conviene llevar todo lo posible al query.

[35:42] En este caso hay bastantes otros filtros, así que podría andar bien. Si tarda mucho, habrá que buscar otra manera. [36:11] Lo que no se puede es que la base aplique el TRUNC por nosotros.

> **Caso especial:** [36:30] La tabla tiene **muchísimos registros**: con algunos rangos de días el Front llega al **timeout**. [37:03] Hay que ver cómo la usa el negocio. Una opción es armar dos operatorias: una de **últimos 30 días** y otra para rangos más largos.

[37:31–38:33] Con TRUNC no se usa el índice por fecha, igual que en el Forms. La solución provisoria funciona pero no es la mejor. Lo ideal es un índice por fecha y la condición ">= desde, < hasta + 1".

### 8. Marcar el campo como no query, Case Restriction, títulos y tarea (41:13 – 45:06)

[40:48–41:43] Que el campo no sea parte del query se indica en la **definición de campos de la tabla** (FD campo actualización [?]), con el indicador de **campo en query** ("in campo query") en **N**. Aunque el campo pertenece a la tabla, al transformarlo con TRUNC ya no se puede filtrar en la base. También se puede modificar desde el Record Group ("rector") o entrando a la tabla.

> **Regla:** [41:43–43:16] Hay que corregir el **Case Restriction** que genera el proceso, porque si no las cosas dejan de funcionar:
> - **number** → NUMBER o MONTO;
> - **varchar** → MIXED, UPPER o LOWER;
> - **date** → DATE. Si se quiere ver con hora, la variante con hora [?] (el audio dice "day/Dave").

> **Regla:** [43:42–44:38] Completar los **títulos (label)** de **todos** los campos, como se ven en el Forms, para que el usuario los reconozca. Conviene hacerlo lo antes posible, aunque el campo no se muestre (ID, IP, subsistema, usuario): al generar después una operatoria, un edit o un insert, el proceso copia el label automáticamente.

[43:42] Este caso de fecha es muy particular. Para una fecha común, desde/hasta queda en el query y es mucho más performante.

**Tarea** [44:38–45:06]:

1. Marcar el campo fecha como **no campo query**, porque se lo transforma.
2. Corregir los tipos de Case Restriction.
3. Completar los títulos por defecto.
4. Acomodar el WHERE de la operatoria con el texto mostrado.

El validador ya está hecho.

## Términos detectados

| Término | Variante en el audio | Qué significa según el video | Timestamp |
|---|---|---|---|
| Valor compuesto | "compuesto", "combinado" | Campo de filtro que recibe dos valores (desde/hasta), numérico o fecha | 1:25, 7:43 |
| JSON del Front | "Jason", "J son", "JAS" | Mensaje con nombre de campo y valor que el Front manda al back | 0:56 |
| Transformador | "transformador" | Convierte el JSON al type generado (mismos nombres de campo) | 0:56 |
| Campo auxiliar de consulta | "campos auxiliares", "fecha aux" | Campos extra (fecha desde/hasta) usados solo para validar | 0:02, 9:41 |
| Obtener valores del JSON fecha | igual | Procedimiento de plantilla que extrae una o dos fechas del JSON | 12:38 |
| Rectype | "Red Type", "reptile", "lock rectype" | Tipo registro que recibe el validador | 11:48, 19:58 |
| Validar operatoria de filtro | igual | Procedimiento donde se validan operatorias y filtros | 18:32 |
| Valida / valida compuesto / no valida | "valida", "el ese de valida" | Opciones de validación del filtro en la parametrización | 28:30 |
| Campo query | "campo query", "in campo query", "parte del query" | Indicador S/N: si el filtro va al WHERE de la base o se filtra después | 35:13, 41:43 |
| TRUNC | "trum", "Trump", "round" | Función que quita la hora; rompe el índice | 30:24 |
| Label | "Live", "ivel" | Título del campo | 44:09 |
| MIXED / UPPER / LOWER | "mixer", "rapper", "lawer" | Valores de Case Restriction para varchar | 42:29, 43:16 |
| DATE | "daite", "Day", "Dave" | Case Restriction para fechas | 42:48 |
| Front | "Frank", "Franco", "foro" | El front del sistema nuevo | 9:41, 31:21 |

## Reglas y casos especiales detectados

- [6:51] El WHERE del bloque del Forms va al filtro de la operatoria, salvo la parte de fechas.
- [7:43] Un filtro desde/hasta sobre un mismo campo se define como campo **compuesto** en la operatoria.
- [9:41] Con campo compuesto, el Front arma el BETWEEN; el back solo usa las dos fechas para validar.
- [15:56] Llamar a "obtener valores del JSON fecha" solo en campos compuestos, por rendimiento.
- [19:58] Validador: recibe rectype y usuario, devuelve error; siempre RETURN después del error; nombre del validador igual al campo.
- [22:41] Si alguna fecha es nula: "Debe ingresar fecha desde y fecha hasta".
- [10:16] Desde ≤ hasta y rango máximo de 30 días (caso log).
- [24:18] El query posterior lo ejecuta el validador automáticamente.
- [25:43] Si el validador modifica otros campos, debe reasignar los valores al JSON (línea final).
- [28:30] Valida = una fecha; valida compuesto = dos fechas + programar type; no valida = dos fechas sin programar.
- [39:33] Con fecha con hora e índice: `fecha >= desde AND fecha < hasta + 1`; nunca TRUNC sobre la columna.
- [35:13] Un campo no query se filtra después de traer los datos: es poco performante.
- [36:30] Tabla de log muy grande: riesgo de timeout; evaluar operatorias por rango (últimos 30 días).
- [42:29] Corregir Case Restriction según el tipo (NUMBER/MONTO, MIXED/UPPER/LOWER, DATE).
- [44:09] Completar el label de todos los campos lo antes posible, porque se copia a las operatorias, edit e insert.

## Pendientes / dudas abiertas

- [0:02, 1:56] Identificador del caso/form: "51736" o "CBKF 517366" [?].
- [2:14, 3:23, 11:48] Nombre exacto de la tabla y del type: ¿Q…_LOG, Q…_LOG_RECTYPE? [?]
- [23:11] Confirmar si el Front copia la primera fecha en la segunda al cargarla.
- [31:50] El instructor dice que "lo tiene que pensar": no hay solución definitiva para filtrar fechas con hora desde el Front sin romper el índice.
- [37:03] Consultar con el negocio cómo usan el filtro, para decidir operatorias por rango.
- [42:48] Valor exacto de Case Restriction para fechas con hora [?].
- [41:13] "FD campo actualización": confirmar el nombre de la tabla de definición de campos [?].
- Nombres mencionados en el audio (sin hablantes identificados): Martín (Martín Olaizola [?]), Ricardo, Bruno.
