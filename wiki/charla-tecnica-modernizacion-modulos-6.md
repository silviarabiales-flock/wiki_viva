---
type: Fuente de video
title: Charla Técnica Modernización de módulos 6 — Usuario de auditoría, validadores por campo y validación de póliza
description: Sesión de revisión sobre una pantalla migrada desde Forms (ramo/póliza/certificado, saldo, estado). Se discute dónde asignar el usuario que hace la transacción en el insert y cómo armar validadores por campo (plantilla "validar campo" llamada desde un único procedimiento "validar registro") que robustecen la validación de póliza, estatus y saldo.
resource: "Transcripciones/Charla tecnica modernizacion 06.docx"
duracion: "0:42:30"
participantes: []
dominio: tecnico
tags: [modernizacion-de-modulos, oracle-forms, migracion, usuario-auditoria, insert, update, validadores, plantilla-validar-campo, validar-registro, post-change, post-query, lista-de-valores, poliza, certificado, saldo, estatus, no-data-found]
estado: borrador
calidad_transcripcion: baja
---

# Charla Técnica Modernización de módulos 6 — Usuario de auditoría, validadores por campo y validación de póliza

## Resumen
- En la pantalla migrada el campo usuario queda editable y no se carga en el insert; en Forms, el usuario real que hace la transacción se asigna "por atrás" antes de insertar, ignorando lo que se tipee. Se acuerda que el usuario no debe poder modificarse ni mostrarse en la definición del insert, y asignarlo antes del insert real (en el procedimiento de validación pre-insert o justo antes del insert), igual que en el update.
- Criterio: todo lo que sea validar o completar datos del mismo registro (sin bloquear) va en el procedimiento de validación previo; el insert propiamente dicho queda para insertar en la tabla (o en otras).
- El productor se saca de la pantalla por indicación del producto (nunca se usó la búsqueda por productor).
- En el alta hay que validar al menos que el registro no exista en la tabla (pre-insert).
- El Forms valida la póliza en el POST-CHANGE del certificado (último campo): está mal, porque el usuario puede volver y cambiar ramo/póliza sin que se revalide, quedando saldo/estatus de otra póliza.
- Patrón del sistema nuevo: un único procedimiento "validar registro" que recibe todos los datos cargados y el nombre del campo a validar; adentro, un `if`/`case` por nombre de campo que llama a un procedimiento por campo armado con la plantilla "validar campo". Lo reutilizable va a una función común.
- Para ramo, póliza y certificado se arma una plantilla cada uno; los tres llaman a un procedimiento común que sólo actúa si sucursal/ramo/póliza/certificado están completos, valida primero que la póliza exista (select del estatus con excepción NO_DATA_FOUND), luego trae el saldo (reutilizando la función de saldo existente) y llena el campo "a amortizar".
- Para el campo Estado (con descriptivo) se pide como tarea implementar las dos alternativas —validador que trae la descripción y lista de valores— y habilitar una u otra para comparar. Los descriptivos de datos ya grabados van en el POST-QUERY.
- Los nombres de validadores deben usar exactamente el nombre del campo (límite de 30 caracteres en nombres de procedimientos).
- El validador de campo sirve en general (~90 % de las veces) tanto para insert como para update; si la lógica difiere, se hace uno propio para update. Tarea final: hacer validadores para todo campo que tenga validate / POST-CHANGE en el Forms.

## Temas
| # | Tema | Desde | Hasta | Dominio |
|---|---|---|---|---|
| 1 | Usuario de auditoría en insert/update: comportamiento del Forms | 0:02 | 5:13 | tecnico |
| 2 | Dónde asignar el usuario: validación pre-insert vs. insert | 5:13 | 8:36 | tecnico |
| 3 | Saldo y productor (se saca el productor) | 8:36 | 9:28 | ambos |
| 4 | Validaciones del alta y el POST-CHANGE del certificado en el Forms | 9:28 | 13:50 | tecnico |
| 5 | Procedimiento único "validar registro" y plantilla "validar campo" | 13:50 | 20:03 | tecnico |
| 6 | Validar desde ramo, póliza y certificado: navegación entre campos | 20:03 | 24:51 | tecnico |
| 7 | Campo Estado: descriptivo, validate vs. lista de valores, POST-QUERY | 24:51 | 30:52 | tecnico |
| 8 | Llamada desde validar registro y nombres de campo | 30:52 | 32:13 | tecnico |
| 9 | Procedimiento común de póliza: existencia, estatus, saldo, NO_DATA_FOUND | 32:13 | 39:09 | ambos |
| 10 | Cierre: criterios generales, reutilización en update y tarea | 39:09 | 42:30 | tecnico |

## Transcripción limpia por tema

### 1. Usuario de auditoría en insert/update: comportamiento del Forms (0:02 – 5:13)
[0:02] Se está probando la pantalla migrada; al moverse a otro registro y volver a entrar, la pantalla no pidió guardar. [0:40] Editar y eliminar ya quedaron, y "lo del Update" ya está hecho. Se va al Forms a mirar el "plainset" [?] (posible trigger de Forms; sin confirmar cuál) y se ve que hace lo mismo con el usuario, igual que el código.

[1:09] Se revisa la parte de insert: en la pantalla nueva no se está insertando el usuario. Cuando se hace el insert se asigna algo a "va para usuario" [?] (posiblemente un campo/variable de usuario), pero no está claro qué valor tiene ahí.

[1:35] Lo que se necesita: guardar el usuario que hace esa transacción (el que modifica o inserta un dato), no el que queda figurando en la tabla. No está claro si el Forms lo carga en el insert.

[2:02] Pregunta: ¿cómo llega el usuario al insertar un registro en el Forms? Al insertar, el usuario se pone automáticamente; en el sistema nuevo no hay (por ahora) manera de ponerlo automático, aunque se podría. Para averiguarlo hay que ejecutar el Forms e intentar insertar un registro, [2:28] o buscar en el código qué hace con el usuario. En la prueba el campo usuario aparece vacío, es decir, no lo llena. Se intenta insertar con datos de prueba (1111, 0 80) y no deja seguir; se prueba con otra póliza.

[3:00] No deja: se rompe por la póliza (otro día se frenó en el certificado). Se recuerda que con Ctrl+F11 se había visto que se podía insertar una misma póliza; ahora ya no lo permite. [3:28] "Endesa" [?] tuvieron que agregar la "prima" [?] (posiblemente la PK). Se pregunta si guardaron el script para pasarlo a test, porque sin él esto no funcionaba; confirman que sí. Por eso ahora no deja repetir una póliza. Se confirma que el usuario realmente no se carga.

[3:54] En la pantalla nueva el usuario es modificable: se puede escribir cualquier cosa en el campo usuario. Lo que se necesita es quién realmente hizo el insert.

[4:23] En la definición del insert hay que establecer que el usuario no se puede modificar, o directamente no mostrarlo: al definir el insert se define qué campos se piden y cuáles son obligatorios (eso ya lo setearon); en esa definición el usuario no debería usarse.

[4:50] El motivo: en el insert se guarda quién hizo la transacción. En el Forms el usuario se manipula "por atrás": no importa lo que se ponga en el campo usuario, se pone el usuario que hizo la transacción.

> **Regla:** El usuario de auditoría debe ser el que realmente hizo la transacción; no debe poder ingresarse ni modificarse en la pantalla (no mostrarlo o dejarlo no modificable en la definición del insert).

### 2. Dónde asignar el usuario: validación pre-insert vs. insert (5:13 – 8:36)
[5:13] Según la programación del Forms, antes de insertar se pone el usuario real, sin importar lo que se haya tipeado; por lo tanto la pantalla nueva está mal: no puede dejar meter cualquier cosa ahí. Consulta: en este proceso, por JSON viaja todo el bloque de datos, que se tiene en el "Red Type" [?] (posiblemente record type).

[5:44] ¿Hay que volver a enviarlo después? No. Hay un procedimiento que se ejecuta antes de insertar (procedimiento de validar insert / pre-insert) y después el insert propiamente dicho. La asignación puede hacerse en ese procedimiento, pero siempre antes de insertar en la tabla: si se pone después, no inserta nada.

[6:13] Opciones: ponerla arriba, antes de hacer el insert, o en el procedimiento "valid pre insert" [?] (el nombre exacto no se recuerda: "valid insert o algo así"). [6:43] Se localiza en el paquete: aparecen "valid predele" [?] y "valid predeces" [?]; ahí se puede poner, o sea, antes de insertar. Ese procedimiento es un validador: antes de insertar se llenan campos, se controla y se da error si falta cargar algo. A veces habrá que ponerlo antes del insert por problemas de performance o para no dejar bloqueado mucho tiempo un registro.

[7:11] Para ser prolijo: todos los datos que no afecten ni bloqueen y que haya que validar o completar van en el validador; una vez que termina, el proceso asigna los valores y después llama al insert, que da la facilidad de insertar en esa tabla, en otra, o hacer lo que haga falta.

[7:41] En este caso el usuario se puede asignar en cualquiera de los dos procedimientos (validador o antes del insert en la tabla real). Lo mejor: así como en el Update se hace en el "pre" [?], en pre-insert también, para que quede uniforme.

[8:02] Ahí va todo lo simple que hace referencia al mismo registro (llenar un campo con otro, etc.). Observación: en la versión actual el campo se seteaba después del insert, por lo que nunca se iba a insertar.

> **Regla:** Asignaciones y validaciones del mismo registro (p. ej. el usuario) van en el procedimiento previo al insert (validación pre-insert) o justo antes del insert en la tabla; nunca después del insert. Mantener el mismo criterio que en el update.

### 3. Saldo y productor (se saca el productor) (8:36 – 9:28)
[8:36] Todo esto (en el Forms) está programado con mucho detalle. Se repasa "lo de saldo": ya lo cargaron. Se pregunta qué trae el productor.

[8:59] El producto dijo que no se ponga ni se cargue el productor: en un momento había dudas de si se podía buscar por productor, pero nunca se hizo y pidió sacarlo. Queda ahora ver qué otras cosas se validan.

> **Regla:** El productor se saca de la pantalla por indicación del producto.

### 4. Validaciones del alta y el POST-CHANGE del certificado en el Forms (9:28 – 13:50)
[9:28] ¿Qué pide el alta? (ramo, póliza…). Como mínimo hay que validar que el registro no exista en la tabla; eso se puede hacer en la validación de pre-insert, porque es genérico.

[10:00] En el Forms, en el certificado hay un POST-CHANGE ("Post Chain"), algo que se usaba en las primeras versiones (muestra lo vieja que es la pantalla). Ahí se valida el certificado, pero deja cargar todo antes, lo cual está mal: el usuario puede volver y cambiar los campos anteriores y no se vuelve a ejecutar. No hay un validador; es muy rústico.

[10:31] En ese POST-CHANGE se trae el saldo y después se consulta el estatus del certificado. El campo "amortizar" se completa según eso; se especula si se habrá hecho en el POST-QUERY, pero no, porque es un dato que se carga en el alta. [10:59] En la implementación nueva lo que hicieron: si ya estaba en 1, se le pone el mensaje a la descripción.

[11:22] Ahí se está cargando una póliza, es decir, un dato: eso va en el validate [?], no en el momento de guardar. Al guardar, el usuario ya tiene todos los registros y se valida/llena lo que se quiera y se salva. [11:52] Esta es otra instancia: el usuario cargó un campo, puso un dato y apretó Tab o Enter; ahí se valida exactamente ese dato. En el POST-CHANGE del certificado se asume que ya se cargó ramo, póliza (y sucursal, que la tiene a mano) y se valida la póliza, pero recién en el último campo.

[12:22] Eso está mal. Lo correcto es hacer una función y preguntar en cada campo: al cargar ramo, si ya están póliza y certificado, validar; al estar en póliza, si ya están ramo y certificado, validar; al estar en certificado, si están sucursal, ramo, póliza, validar. Porque si se carga un certificado correcto, se avanza, y después se vuelve y se cambia la póliza, no hay ninguna validación en póliza. [12:51] No hay validación en el ítem póliza, así que queda validado con un estatus incorrecto. Es una misma validación: si se tienen sucursal, ramo, póliza y certificado (cuatro, o tres porque la sucursal es fija; "si es 80 sería dos" [?]), se ejecuta.

[13:22] Con todos los valores, se cambia el estatus y se carga el saldo, pero en el momento en que el usuario carga el dato en un campo, no en la validación de datos al guardar. [13:50] Por lo tanto va en el validador de insert: ir al paquete; hay un procedimiento validador. Siempre conviene ir primero a la especificación del paquete, que es cortita, para tener todo junto y entender qué hay.

> **Regla:** En el alta validar como mínimo que el registro no exista en la tabla (pre-insert).
> **Caso especial:** En el Forms la póliza se valida sólo en el POST-CHANGE del certificado; si el usuario vuelve y cambia ramo o póliza, no se revalida y queda con saldo/estatus de otra póliza. En el sistema nuevo la validación debe dispararse desde cada uno de los campos de la clave.

### 5. Procedimiento único "validar registro" y plantilla "validar campo" (13:50 – 20:03)
[14:19] Procedimiento "validar registro". También habría que validar la póliza al hacer update ("ampletear" [?]) del registro, pero parece que la póliza no se puede modificar en update, así que no hay que hacer nada; se recuerda que en el update sólo se podían cambiar dos campos (uno era el Estado). Ahora se está en el insert, así que se valida para insert.

[14:48] El procedimiento es "validar … generación de registro" [?] ("validar Henry Head"). Se llama cada vez que el usuario se para en un campo, por ejemplo cuando pone un ramo. [15:19] Se recuerda el "check se valida" [?] del campo en la definición del insert. Se llama al procedimiento con todos los datos que cargó el usuario hasta ese momento y con el nombre del campo a validar (p. ej. ramo); del lado propio se decide: si es ramo, hago esto; si es póliza, esto; si es certificado, esto.

[15:48] Es un único procedimiento, que se llama muchas veces (continuamente, al pararse en cada campo), y recibe por parámetro qué campo validar. [16:16] Se aclara una confusión con la LOV: se puede traer una lista y validar ambas cosas (mostrar la lista y, cuando el usuario elige un dato, validar ese campo). [16:45] La "lista genérica" tiene la misma idea: "dame la lista de tal campo" (pide de qué campo y devuelve); aquí es "valídame este campo, tomá todo lo que cargó el usuario hasta ahora".

[17:12] A medida que el usuario aprieta Tab por cada campo se llama a "validar registro"; en vez de tener 70 procedimientos hay uno solo con la lógica adentro. [17:42] Propuesta: hacer una función con la lógica actual y llamarla cuando ramo, sucursal (seteada), póliza y certificado estén completos (no nulos). [18:11] Asigna el valor (p. ej. 1). La idea está bien, pero hay que acomodarla: a "validar registro" le pueden llegar 75 campos; meter toda la lógica ahí no es viable.

[18:40] Conviene un `case` o `if` por nombre del campo. Existe una plantilla "validar campo" (armada por el expositor, visible en el paquete): por cada campo a validar se hace un procedimiento con esa plantilla. [19:07] Si algún campo reutiliza código, eso va en una función. En "validar registro" sólo debe haber: si es ramo, llamo a validar ramo; si es póliza, llamo a validar póliza; etc. (va y viene, porque después se actualiza).

[19:37] Primero definir qué se valida: en el insert, cuando el usuario pone el ramo, la póliza y el certificado. [20:03] Se hacen esas tres plantillas, y las tres llaman a un único procedimiento/función común.

> **Regla:** Un único procedimiento "validar registro" recibe todos los datos cargados y el nombre del campo; dentro sólo un `if`/`case` por nombre de campo que llama a un procedimiento por campo (plantilla "validar campo"). La lógica compartida va a una función/procedimiento común.

### 6. Validar desde ramo, póliza y certificado: navegación entre campos (20:03 – 24:51)
[20:27] Duda: por qué llamar a la función también desde ramo y póliza, si para traer el estatus se necesitan ramo, póliza y certificado. [20:45] Respuesta: el usuario pone ramo 4; se llama a validar ramo, que pregunta si están ramo, póliza y certificado. [21:13] La primera vez no hay nada y no hace nada. Después carga la póliza; el validador de póliza ve ramo y póliza, pero falta certificado: devuelve OK. Luego pone el certificado: [21:41] ya tiene ramo, póliza y certificado y llena los campos. Si después el usuario vuelve y cambia ramo 4 por ramo 2 (puede moverse entre campos), [22:07] al caer en validar ramo ya tiene ramo, póliza y certificado, pero es otra póliza/otro certificado, que puede no existir.

[22:35] El Forms no lo preveía: se podía cargar póliza y certificado, traer los datos, después modificar la póliza y quedaban los datos (saldo, etc.) de la póliza anterior, sin que el certificado lo frenara.

[22:56] Se decide hacer ahora las plantillas y el procedimiento, e ir agregando otras validaciones. [23:22] La plantilla original "validar campo" se deja como ejemplo y se copia para cada campo. Para ramo se usa el nombre del campo: [23:52] "va para" / "Mapa" [?] (nombre de campo dudoso); se discute el nombre del procedimiento: "validate" + nombre del campo.

[24:16] Luego lo mismo para póliza y certificado. Hay que hacer un validador por cada campo que tenga validación en el Forms (también el Estado).

> **Caso especial:** Si el usuario completa ramo/póliza/certificado y luego vuelve a cambiar uno de ellos, el validador de ese campo debe revalidar todo con la nueva combinación (la póliza puede no existir).

### 7. Campo Estado: descriptivo, validate vs. lista de valores, POST-QUERY (24:51 – 30:52)
[24:51] Ya están los tres validadores (ramo, póliza, certificado). Además está el estatus/Estado, que en el Forms tiene un POST-CHANGE que trae el descriptivo cuando el usuario pone el Estado. No tiene lista de valores en el bloque. Se revisa en el canvas: [25:22] parado en el campo Estado, a la izquierda aparecen sus triggers ("intriga" [?]); cuando el usuario mete un Estado, carga la descripción.

[25:44] Dos maneras de hacerlo: agregar una lista de valores donde pueda elegir el Estado, o hacerlo en el validate del Estado, que carga la descripción. Este campo era el que se podía modificar (en update). [26:15]–[26:41] La descripción del Estado sí se trae, pero en consulta; ahora se está insertando.

[26:41] Ejemplo en el Forms: al insertar se pone un productor (p. ej. 109) y trae el nombre, sea por validate o por lista de valores. [27:07] Eso es distinto del POST-QUERY: en el POST-QUERY se trae lo que ya está en la base (ya tengo el productor y traigo el nombre); acá el usuario carga el código y hay que traerle el nombre al costado. Con el Estado: pone 1, aprieta Tab y quiere ver la descripción.

[27:31] Son dos cosas distintas: si existe el descriptivo, es obligatorio tenerlo en el POST-QUERY. Todos los datos descriptivos se traen en el POST-QUERY (donde se llenan los campos al consultar). Al insertar, en cambio, todo está vacío: [28:01] se da la lista de valores y se agrega la descripción al elegir, o en el validate se llena el otro campo, como hace el POST-CHANGE del Estado. Valores posibles del Estado: 1 o 2 (por decir). En el Forms, si es no nulo lo busca y si no lo encuentra no da error, lo cual también está mal. [28:31] Hay que preguntar qué pasa en ese caso; por ahora, si no está en el Record Group ("red Code"), se debería dar error.

[28:31]–[29:27] Se señala que el equipo está aprendiendo a la vez Forms y a migrar (quienes migran no trabajaron en Forms más allá de arreglos puntuales), por eso se revisa en conjunto. [29:27] Para el Estado también podrían hacer la plantilla "validar Estado" y llenar la descripción cuando el usuario lo carga, o darle la lista de valores; el expositor prefiere la lista de valores cuando son pocos valores. [29:53] Pero para que aprendan, se pide hacer un validate que traiga un descriptivo y ver cómo, al poner a mano un número, se llena el dato de al lado pasando por el validador de "generación de registro" [?].

[30:21] Tarea: con las plantillas, hacer la del certificado, la de validar Estado (que lleve el Estado al descriptivo) y también la lista de valores para lo mismo; [30:52] habilitar una y deshabilitar la otra para ver cómo trabaja.

> **Regla:** Todo dato descriptivo debe cargarse en el POST-QUERY (consulta de datos existentes); al insertar, el descriptivo se llena por validador del campo o al elegir de una lista de valores.
> **Regla:** Si el valor ingresado no existe en su Record Group/lista, se debe dar error (el Forms no lo hace; a confirmar).
> **Caso especial:** Para pocos valores se prefiere lista de valores; para el Estado se pide implementar ambas alternativas y comparar.

### 8. Llamada desde validar registro y nombres de campo (30:52 – 32:13)
[30:52] Después de armar las plantillas "validar tal cosa", hay que llamarlas desde "validar registro". El nombre del campo que viene por parámetro tiene que coincidir. [31:17] Se comenta que "validate" + nombre es largo: en los nombres de procedimientos no se pueden poner más de 30 caracteres; se deja así. Hay que poner exactamente el nombre del campo para asegurar que se valida el campo correcto y que coincide con el nombre que viene en el parámetro, [31:44] porque habrá campos parecidos que pueden confundir. En "validar registro" va un `if nombre_campo = …` (estado, póliza, etc.) que llama al validador correspondiente; después se hace el procedimiento común (no el genérico que se llama desde otros lugares).

> **Regla:** El nombre del procedimiento validador debe contener exactamente el nombre del campo, coincidente con el nombre que llega por parámetro (respetando el límite de 30 caracteres).

### 9. Procedimiento común de póliza: existencia, estatus, saldo, NO_DATA_FOUND (32:13 – 39:09)
[32:13] El procedimiento común es el que valida la póliza y trae el saldo y los datos de la póliza (lo que se llenaba en el certificado). [32:39] Es muy parecido a la plantilla: recibe el record por parámetro, llena los campos, lo devuelve y da error si corresponde. Lo primero: preguntar si están todos los datos (ramo, póliza, certificado); si no, no hace nada, porque se lo llama desde distintos lugares donde pueden no estar completos. [33:08] Si no están todos, `return` y listo, sin validar nada. Se consulta "Martín" [?]; el saldo también se llama desde ahí.

[33:33] ¿No conviene una función que devuelva el saldo? Ya existe: hay que llamarla adentro, reutilizándola. [34:02] El saldo de la póliza ya está resuelto, se llama desde unos 40 lugares distintos y ya tiene los grants ("gran" [?]); no se reimplementa. Lo primero a validar es que la póliza exista, no al revés (traer el saldo antes). [34:30] Si no existe, el saldo vendría nulo; por eso primero hay que fijarse que la póliza exista. Al entrar al procedimiento ya están todos los datos, porque previamente se valida en "validar".

[35:00] En el camino feliz (ramo, póliza, certificado en orden) trae saldo y estatus y llena todo. [35:27] Pero si después se cambia el número de póliza o el ramo, la combinación puede no existir: p. ej. un número de póliza de automotores (ramo 111 [?], números grandes) y luego se cambia a ramo 1: no existe, y al validar no va a traer saldo. [35:54] El problema no es el camino feliz sino permitir modificar un dato que repercute en obtener el saldo. [36:25] Incluso en el camino feliz puede no estar. Hay casos en que no hace falta certificado: al encontrar la póliza se sabe que no lo necesita y debería cargarse automáticamente (eso existe en la parte de cobranza: según el caso se pide certificado o no). [36:53] No se va a llegar a ese nivel ahora, pero si se permite ir y venir entre campos, el proceso tiene que ser robusto y subsanar esos errores en la función.

[37:23] A grandes rasgos: con todos los datos, fijarse si la póliza existe ("carnet de certificado", "rango" [?]), traer el saldo y el estatus. Lo primero en la función es el select del estatus, con manejo de NO_DATA_FOUND ("no data phone"). [37:51] La función pregunta: ¿tengo sucursal, ramo, póliza y certificado? Si sí, busca el estatus de ese certificado; si se ingresó cualquier cosa no lo encuentra y se da error ("póliza incorrecta" o similar). Una vez obtenido el estatus, se obtiene el saldo y se llena el campo "a amortizar" ("mapa a amortizar" [?]). [38:23] Con eso se resuelve: si el estatus es nulo se da error; si es "111 o 15" [?] se carga "va para amortizar" [?].

[38:41] Corrección: el select no devuelve nulo si no encuentra, sino que levanta la excepción NO_DATA_FOUND; hay que poner `exception when no_data_found`. Un valor nulo se obtiene con MAX o MIN cuando no hay filas. [39:09] Usar MAX/MIN así está mal programado, porque si el campo realmente es nulo no se distingue entre "no existe" y "existe con nulo".

> **Regla:** El procedimiento común sólo actúa si están todos los datos de la clave (sucursal/ramo/póliza/certificado); si no, `return` sin validar.
> **Regla:** Primero validar que la póliza exista (select del estatus con `exception when no_data_found` → error); recién después obtener el saldo (reutilizando la función de saldo existente) y llenar el campo "a amortizar".
> **Regla:** No usar MAX/MIN para evitar NO_DATA_FOUND: no permite distinguir "no existe" de "existe con nulo".
> **Caso especial:** Hay pólizas que no requieren certificado (en cobranza se resuelve automáticamente); queda fuera del alcance por ahora.

### 10. Cierre: criterios generales, reutilización en update y tarea (39:09 – 42:30)
[39:09] Con eso alcanza, aunque faltan algunas cosas y hay que seguir mirando ("triguela" [?]). [39:39] Recorrer la pantalla y verificar que se comporte más o menos igual que el Forms. Esta pantalla es simple (3 o 4 campos); empezarán a aparecer las complicadas. Se menciona "tasa de cambio", una que quiere todo el mundo y que se podría sacar fácil.

[40:08] Criterio: una plantilla de validación por cada campo, sin código esparcido por todos lados. Así como el Forms tiene su POST-CHANGE para validar un campo, en el sistema nuevo habrá un procedimiento por campo; lo que se reutilice desde ahí es aparte, pero hay que tener claro qué valida cada uno. [40:37] Esto sirve para lo que viene, no sólo para esta pantalla.

[41:10] En el Forms hay un solo validador por campo, que se llama tanto para insert como para update. Por lo tanto, si ya existe el validador de un campo, se lo puede llamar al validar en un update, salvo que la lógica difiera; en ese caso se hace un procedimiento propio del campo para update. [41:39] El 90 % de las veces es el mismo validador (p. ej. cambiar un ramo por otro: verificar que el ramo exista, en ambos casos).

[42:10] Tarea: hacer todos los validadores que encuentren; cada campo que en el Forms tenga un validate o un POST-CHANGE ("postchet") con lógica lleva su procedimiento. Después se ve cómo se ordenan.

> **Regla:** Un procedimiento validador por cada campo que tenga validación (validate/POST-CHANGE) en el Forms; nada de código suelto.
> **Regla:** El mismo validador de campo se reutiliza en insert y update salvo que la lógica difiera (≈90 % de los casos es el mismo).

## Términos detectados
| Término | Variante en el audio | Qué significa según el video | Timestamp |
|---|---|---|---|
| Forms / Oracle Forms | "Phone", "Font", "fon", "fam", "Fam", "phone", "form", "forma" | La pantalla vieja que se migra | 0:40, 2:02, 5:13, 22:07, 26:41, 41:10 |
| Usuario (auditoría) | "usuario" | Usuario que hizo la transacción; en Forms se asigna antes de insertar ignorando lo tipeado | 1:35, 4:50, 5:13 |
| Definición del insert | "definición del insert" | Configuración en el sistema nuevo de qué campos se piden y cuáles son obligatorios en el alta | 4:23 |
| Validación pre-insert | "valid pre insert", "validar insertes", "valid pre" | Procedimiento del paquete que corre antes del insert: valida y completa datos | 5:44, 6:13 |
| valid predele / valid predeces | "valid predele", "valid predeces" | Procedimientos vistos en el paquete (¿pre-delete?) [?] | 6:43 |
| Red Type | "l Red Type" | Estructura donde viaja el bloque de datos por JSON (¿record type?) [?] | 5:13 |
| POST-CHANGE | "Post Chain", "post Chain", "poché", "postchain", "post change", "postchet" | Trigger de Forms a nivel campo usado para validar/traer descriptivo; "de las primeras versiones" | 10:00, 11:52, 24:51, 40:08, 42:10 |
| POST-QUERY | "post Query", "post Cueri" | Trigger de Forms donde se traen los descriptivos de datos ya grabados | 10:31, 27:07, 27:31 |
| validate (validador de campo) | "balidate", "validay", "valyday", "validez", "validate" | Validación al ingresar un dato en un campo (Tab/Enter); en Forms y en el sistema nuevo | 11:22, 26:41, 28:01, 29:53 |
| Validar registro | "validar el registro", "validar registros", "validar Henry Head validar generación de registro" | Procedimiento único que recibe los datos cargados y el nombre del campo a validar | 14:19, 14:48, 19:07, 30:52 |
| Plantilla "validar campo" | "plantilla validar campo", "plantilla" | Plantilla de procedimiento validador por campo, se copia por cada campo | 18:40, 23:22 |
| Lista genérica | "lista genérica" | Procedimiento que devuelve la lista (LOV) de un campo dado | 16:45 |
| LOV / lista de valores | "Love", "lista de valores" | Lista de valores para elegir un dato | 16:16, 25:44, 29:27 |
| Record Group | "red Code" | Origen de valores válidos del Estado | 28:31 |
| Estado / estatus | "Estado", "estatus" | Campo con descriptivo (valores 1 o 2); estatus del certificado | 10:31, 24:51, 28:01 |
| Saldo | "saldo" | Saldo de la póliza; función existente llamada desde ~40 lugares | 8:36, 34:02 |
| Amortizar | "amortizar", "mapa a amortizar", "va para amortizar" | Campo que se llena según estatus; nombre exacto [?] | 10:31, 37:51, 38:23 |
| Sucursal / ramo / póliza / certificado | "sucursal ramo police certificado", "Rambo", "rabo", "polis" | Clave de la póliza; la sucursal es fija | 12:51, 37:51 |
| NO_DATA_FOUND | "no data phone", "no data fan", "nuevo data fan" | Excepción cuando el select no encuentra fila | 37:23, 38:41 |
| MAX / MIN | "Max", "min", "Max Min" | Funciones que devuelven nulo sin filas; desaconsejado para esto | 38:41, 39:09 |
| Grants | "los gran" | Permisos ya otorgados a la función de saldo [?] | 34:02 |
| Canvas | "canvas" | Lienzo de Forms donde se ve el campo Estado | 24:51, 25:22 |
| Productor | "productor" | Campo que se saca por indicación del producto | 8:59, 26:41 |
| Tasa de cambio | "tasa de cambio" | Otra pantalla/tabla mencionada como fácil de migrar | 39:39 |
| Cobranza | "cobranza" | Área donde se resuelve automáticamente si una póliza requiere certificado | 36:25 |
| Ctrl+F11 | "control F 11" | Atajo usado en la prueba (en Forms) | 3:00 |
| Test | "test" | Ambiente al que se pasó el script | 3:28 |

## Reglas y casos especiales detectados
- [1:35] Se debe guardar el usuario que realmente hace la transacción.
- [4:23] En la definición del insert, el usuario no debe poder modificarse o no debe mostrarse.
- [5:13] En Forms, antes de insertar se asigna el usuario real, ignorando lo ingresado.
- [5:44] La asignación del usuario va antes del insert en la tabla; después no inserta nada.
- [6:43] A veces conviene asignar antes del insert por performance o para no bloquear registros.
- [7:11] Validaciones y completado de datos que no bloqueen van en el validador previo; luego el insert.
- [7:41] Mismo criterio en update y en pre-insert.
- [8:59] El productor se saca de la pantalla (indicación del producto).
- [9:28] En el alta validar que el registro no exista en la tabla (pre-insert).
- [10:00] Caso especial: Forms valida póliza sólo en POST-CHANGE del certificado; cambiar ramo/póliza después no revalida.
- [12:22] La validación de póliza debe dispararse desde ramo, póliza y certificado, cuando estén todos los datos.
- [13:50] Revisar primero la especificación del paquete.
- [17:12] Un único "validar registro" en vez de un procedimiento por llamada; dentro, un if/case por nombre de campo.
- [19:07] Un procedimiento por campo (plantilla "validar campo"); código reutilizable en funciones.
- [22:07] Caso especial: volver a cambiar el ramo con póliza y certificado cargados implica revalidar otra póliza que puede no existir.
- [27:31] Los descriptivos de datos grabados se traen en el POST-QUERY (obligatorio si existe descriptivo).
- [28:31] Si el Estado no está en el Record Group, se debería dar error (a confirmar).
- [29:27] Preferencia por lista de valores cuando son pocos valores.
- [31:17] Nombre del validador = nombre exacto del campo; máximo 30 caracteres en nombres de procedimientos.
- [32:39] El procedimiento común no hace nada (return) si faltan datos de la clave.
- [34:02] Reutilizar la función de saldo existente; no reimplementarla.
- [34:30] Primero validar existencia de la póliza, después traer saldo.
- [36:25] Caso especial: pólizas sin certificado (resuelto en cobranza); fuera de alcance.
- [38:41] Usar exception NO_DATA_FOUND; un select sin filas no devuelve nulo.
- [39:09] No usar MAX/MIN para obtener nulo: no distingue inexistente de nulo.
- [40:08] Un validador por campo, sin código disperso.
- [41:10] El validador de campo sirve para insert y update salvo que la lógica difiera (~90 % igual).
- [42:10] Hacer validadores para todo campo con validate o POST-CHANGE en el Forms.

## Pendientes / dudas abiertas
- [0:40] "plainset": ¿qué trigger/procedimiento del Forms es? [?]
- [1:09] "va para usuario": nombre del campo/variable de usuario [?]
- [2:28] Datos de prueba "1111", "cero 80": ¿sucursal 80? [?]
- [3:28] "Endesa" y "poner la prima": ¿se agregó la PK para impedir pólizas duplicadas? [?]
- [5:13] "Red Type": ¿record type / %ROWTYPE? [?]
- [6:43] Nombres exactos de los procedimientos "valid pre insert", "valid predele", "valid predeces" [?]
- [7:41] "en el pre de" del Update: ¿pre-update? [?]
- [10:59] Lógica del campo amortizar: "si está en 1 se pone el mensaje a descripción" — confirmar.
- [12:51] "si es 80 sería dos" (sucursal fija) [?]
- [14:19] "ampletear": ¿hacer update? Confirmar que la póliza no es modificable en update y qué dos campos sí (uno es el Estado).
- [14:48] Nombre exacto del procedimiento "validar … generación de registro" [?]
- [15:19] "check en se valida": ¿check "se valida" en la definición del campo? [?]
- [23:52] Nombre del campo "va para" / "Mapa" [?]
- [25:22] "intriga a la izquierda": ¿triggers del ítem en el navegador de Forms? [?]
- [28:31] Qué hacer si el Estado no existe en el Record Group: hay que preguntar (Forms no da error).
- [30:21] Tarea: plantillas de certificado y validar Estado + LOV de Estado; comparar.
- [33:08] "consulto Martín" [?]
- [34:02] "los gran": ¿grants? [?]
- [35:27] "viene el flanco" [?]; "ramo 111" de automotores [?]
- [37:23] "carnet de certificado", "si está de ahí a rango" [?]
- [37:51]/[38:23] Nombre del campo "mapa/va para amortizar" y valores "111 o 15" que lo activan [?]
- [39:09] "triguela" [?]
- [39:39] Tasa de cambio: pantalla candidata a migrar próximamente.
- [42:10] Tarea: hacer todos los validadores de campos con validate / POST-CHANGE.
