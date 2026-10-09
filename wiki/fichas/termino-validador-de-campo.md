---
type: Término
title: Validador de campo
description: Procedimiento por campo, armado con la plantilla "validar campo", que valida el dato apenas el usuario lo carga y que se llama desde un único procedimiento "validar registro".
aliases: [validador, validate, "validar campo", "validar registro", "validar generación de registro", "balidate", "validay", "valyday", "validez", "validar Henry Head"]
dominio: tecnico
tags: [validadores, plantilla-validar-campo, validar-registro, post-change, insert, update, rectype, return, json, oracle-forms, migracion]
estado: borrador
valida: referente técnico
fuentes: [charla-tecnica-modernizacion-modulos-6@11:52, charla-tecnica-modernizacion-modulos-6@15:19, charla-tecnica-modernizacion-modulos-6@18:40, charla-tecnica-modernizacion-modulos-6@31:17, charla-tecnica-modernizacion-modulos-6@41:10, capacitacion-validacion-compuesta-campo-fecha-2026-05-12@19:58, capacitacion-validacion-compuesta-campo-fecha-2026-05-12@25:43, charla-tecnica-modernizacion-modulos-4@1:29:13]
ultima_fuente: 2026-05-12
contradicciones: 0
---

# Validador de campo

## Definición
Un validador de campo valida exactamente el dato que el usuario acaba de cargar en un campo, en el momento en que aprieta Tab o Enter, y no al guardar el registro completo [Charla 6 · 11:52](../charla-tecnica-modernizacion-modulos-6.md). Cargar un dato como la póliza va en el validate y no en el momento de guardar [Charla 6 · 11:22](../charla-tecnica-modernizacion-modulos-6.md).

En el sistema nuevo hay un único procedimiento "validar registro", que se llama con todos los datos que cargó el usuario hasta ese momento y con el nombre del campo a validar [Charla 6 · 15:19](../charla-tecnica-modernizacion-modulos-6.md). Adentro va un `case` o `if` por nombre de campo, y por cada campo a validar se hace un procedimiento con la plantilla "validar campo" [Charla 6 · 18:40](../charla-tecnica-modernizacion-modulos-6.md). Lo que se reutiliza entre campos va en una función, y en "validar registro" solo queda "si es ramo, llamo a validar ramo; si es póliza, llamo a validar póliza" [Charla 6 · 19:07](../charla-tecnica-modernizacion-modulos-6.md).

Es el equivalente del POST-CHANGE del Forms: así como el Forms tiene su POST-CHANGE para validar un campo, en el sistema nuevo hay un procedimiento por campo [Charla 6 · 40:08](../charla-tecnica-modernizacion-modulos-6.md). Cada campo que en el Forms tenga un validate o un POST-CHANGE con lógica lleva su procedimiento validador [Charla 6 · 42:10](../charla-tecnica-modernizacion-modulos-6.md).

## Detalle
- "Validar registro" es un solo procedimiento que se llama muchas veces (al pararse en cada campo) y recibe por parámetro qué campo validar [Charla 6 · 15:48](../charla-tecnica-modernizacion-modulos-6.md).
- En vez de tener 70 procedimientos hay uno solo, que se llama cada vez que el usuario aprieta Tab [Charla 6 · 17:12](../charla-tecnica-modernizacion-modulos-6.md); pero meter toda la lógica en "validar registro" no es viable, porque le pueden llegar 75 campos [Charla 6 · 18:11](../charla-tecnica-modernizacion-modulos-6.md).
- La plantilla original "validar campo" se deja como ejemplo y se copia para cada campo [Charla 6 · 23:22](../charla-tecnica-modernizacion-modulos-6.md).
- **Nombre igual al campo:** el procedimiento se nombra "validate" + nombre del campo [Charla 6 · 23:52](../charla-tecnica-modernizacion-modulos-6.md). Hay que poner exactamente el nombre del campo, coincidente con el que llega por parámetro, respetando el límite de 30 caracteres de los nombres de procedimiento [Charla 6 · 31:17](../charla-tecnica-modernizacion-modulos-6.md). Esto evita confusiones con campos parecidos, y en "validar registro" va un `if nombre_campo = …` que llama al validador correspondiente [Charla 6 · 31:44](../charla-tecnica-modernizacion-modulos-6.md). La Capacitación repite que cada validador debe llevar el nombre del campo que valida [Capacitación · 19:58](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- **Formato:** el validador recibe el rectype (un solo registro ya cargado desde el JSON) y el usuario, por si hace falta, y devuelve si hay error o no [Capacitación · 19:58](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). En la Charla 6 el procedimiento común de póliza se describe "muy parecido a la plantilla": recibe el record por parámetro, llena los campos, lo devuelve y da error si corresponde [Charla 6 · 32:39](../charla-tecnica-modernizacion-modulos-6.md).
- **RETURN:** después de cargar un error hay que poner siempre RETURN; si no, una mala programación puede seguir ejecutando y terminar "todo bien" cuando no lo está [Capacitación · 19:58](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). También se usa `return` sin validar nada cuando no están todos los datos que el procedimiento necesita [Charla 6 · 33:08](../charla-tecnica-modernizacion-modulos-6.md).
- Si las validaciones de un mismo dato son muy distintas, se pueden separar ("validar fecha 1", "validar fecha 2") o dejar en un solo procedimiento discriminando por tipo [Capacitación · 20:52](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- Al copiar la lógica del Forms, las referencias `:bloque.campo` se reemplazan por los campos del registro [Capacitación · 21:48](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- En un validador de filtro no hay que programar la ejecución del query posterior (el GO_BLOCK / EXECUTE_QUERY del Forms): la hace el validador automáticamente [Capacitación · 24:18](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- **Validadores que modifican otros campos:** a veces el validador, si llega un dato, tiene que completar otro campo [Capacitación · 25:09](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). En ese caso (por ejemplo, si busca compañía, sucursal o agencia y los carga) tiene que ejecutar al final la línea que reasigna los valores modificados al JSON y los devuelve; si solo valida, no hace falta, y con varios validadores hay que ubicar esa línea de modo que no se pierdan cambios [Capacitación · 25:43](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). Para probarlo, se asigna un valor a algún campo dentro del validador y se verifica que vuelva [Capacitación · 26:35](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- Ejemplos de validadores que llenan otros campos en la Charla 6: el validate del Estado que llena la descripción, como hacía el POST-CHANGE del Estado [Charla 6 · 28:01](../charla-tecnica-modernizacion-modulos-6.md), y el procedimiento común de póliza que, obtenido el estatus, trae el saldo y llena el campo "a amortizar" [Charla 6 · 37:51](../charla-tecnica-modernizacion-modulos-6.md).
- **Insert y update:** en el Forms hay un solo validador por campo que se llama para insert y para update, así que si ya existe el validador de un campo se lo llama también en el update, salvo que la lógica difiera, en cuyo caso se hace uno propio para update [Charla 6 · 41:10](../charla-tecnica-modernizacion-modulos-6.md). El 90 % de las veces es el mismo validador (por ejemplo, verificar que el ramo exista) [Charla 6 · 41:39](../charla-tecnica-modernizacion-modulos-6.md). En la pantalla de la póliza no hizo falta validar en update porque parece que la póliza no se puede modificar en update [Charla 6 · 14:19](../charla-tecnica-modernizacion-modulos-6.md).
- **Por qué no alcanza el POST-CHANGE del Forms:** en el Forms la póliza se valida en el POST-CHANGE del certificado, dejando cargar todo antes; si el usuario vuelve y cambia campos anteriores, no se revalida [Charla 6 · 10:00](../charla-tecnica-modernizacion-modulos-6.md). Lo correcto es preguntar desde cada campo de la clave si ya están los otros y, en ese caso, validar [Charla 6 · 12:22](../charla-tecnica-modernizacion-modulos-6.md). Si el usuario cambia el ramo con póliza y certificado ya cargados, el validador de ramo revalida otra combinación, que puede no existir [Charla 6 · 22:07](../charla-tecnica-modernizacion-modulos-6.md).
- Validador y lista de valores no se excluyen: se puede mostrar la lista y, cuando el usuario elige, validar ese campo [Charla 6 · 16:16](../charla-tecnica-modernizacion-modulos-6.md). La "lista genérica" sigue la misma idea ("dame la lista de tal campo"), mientras que aquí es "valídame este campo, tomá todo lo que cargó el usuario" [Charla 6 · 16:45](../charla-tecnica-modernizacion-modulos-6.md).
- No confundir con la validación pre-insert, el procedimiento que corre antes del insert, llena campos, controla y da error si falta algo [Charla 6 · 6:43](../charla-tecnica-modernizacion-modulos-6.md).
- **Contexto de filtro:** en la Capacitación, el validador de fecha se llama desde el procedimiento del paquete "validar operatoria de filtro", que valida las operatorias y los filtros definidos [Capacitación · 18:32](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). Es otro momento (filtro de una operatoria) distinto del alta campo por campo de la Charla 6 [Charla 6 · 19:37](../charla-tecnica-modernizacion-modulos-6.md).
- En la Charla 4 quedó pendiente recorrer los validadores de cada campo del Forms [Charla 4 · 1:28:48](../charla-tecnica-modernizacion-modulos-4.md): mirar qué se valida en cada campo y saber en qué punto ponerlo [Charla 4 · 1:29:13](../charla-tecnica-modernizacion-modulos-4.md).

## Contradicciones
Sin contradicciones entre las fuentes.

## Relacionados
- [Valor compuesto](termino-valor-compuesto.md)
- [Usuario de auditoría](regla-usuario-de-auditoria.md)
- [Lista de valores](termino-lista-de-valores.md)
- [Descriptivo y POST-QUERY](termino-descriptivo-y-post-query.md)
- [Ref Code y Record Group](termino-ref-code-y-record-group.md)

## Fuentes
| Video | Fecha | Minuto | Qué aporta |
|---|---|---|---|
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 1:28:48, 1:29:13 | Validadores de cada campo del Forms quedan pendientes |
| [Charla 6](../charla-tecnica-modernizacion-modulos-6.md) | 2026-04-23 | 6:43, 10:00, 11:22, 11:52, 12:22 | Validación al cargar el dato vs. al guardar; falla del POST-CHANGE del certificado |
| [Charla 6](../charla-tecnica-modernizacion-modulos-6.md) | 2026-04-23 | 14:19, 15:19, 15:48, 16:16, 16:45, 17:12, 18:11, 18:40, 19:07, 19:37 | Procedimiento único "validar registro" y plantilla "validar campo" |
| [Charla 6](../charla-tecnica-modernizacion-modulos-6.md) | 2026-04-23 | 22:07, 23:22, 23:52, 28:01, 31:17, 31:44 | Revalidación al volver a un campo; copia de plantilla; nombre igual al campo |
| [Charla 6](../charla-tecnica-modernizacion-modulos-6.md) | 2026-04-23 | 32:39, 33:08, 37:51, 40:08, 41:10, 41:39, 42:10 | Formato del procedimiento común; uso en insert y update; POST-CHANGE como origen |
| [Capacitación](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md) | 2026-05-12 | 18:32, 19:58, 20:52, 21:48, 24:18 | "Validar operatoria de filtro"; formato rectype/usuario/error; RETURN; nombre del campo |
| [Capacitación](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md) | 2026-05-12 | 25:09, 25:43, 26:35 | Validadores que modifican otros campos y reasignación al JSON |
