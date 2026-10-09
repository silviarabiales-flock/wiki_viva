---
type: Término
title: Descriptivo y POST-QUERY
description: Campo descriptivo es el que muestra la descripción al lado de un código; en Forms se llena en el POST-QUERY y en el sistema nuevo se trae por join o se completa en el paquete.
aliases: [descriptivo, campo descriptivo, desc, "desc lista pro", "DESP lista pro", POST-QUERY, post-query, "post Quei", "post Cueri", "Post Code", "postcuel", Column Mapping, "Column Mapy"]
dominio: tecnico
tags: [modernizacion-de-modulos, descriptivos, post-query, column-mapping, lov, record-group, paquete, type, join, oracle-forms]
estado: borrador
valida: referente técnico
fuentes: [charla-tecnica-modernizacion-modulos-4@10:43, charla-tecnica-modernizacion-modulos-4@56:48, charla-tecnica-modernizacion-modulos-4@57:12, charla-tecnica-modernizacion-modulos-6@27:31, charla-tecnica-modernizacion-modulos-4@6:29, charla-tecnica-modernizacion-modulos-4@6:02, charla-tecnica-modernizacion-modulos-4@7:23, charla-tecnica-modernizacion-modulos-4@7:52, charla-tecnica-modernizacion-modulos-4@6:53, charla-tecnica-modernizacion-modulos-4@3:14, charla-tecnica-modernizacion-modulos-6@27:07, charla-tecnica-modernizacion-modulos-6@28:01, charla-tecnica-modernizacion-modulos-6@10:31, charla-tecnica-modernizacion-modulos-4@9:19, charla-tecnica-modernizacion-modulos-4@9:45, charla-tecnica-modernizacion-modulos-4@5:07, charla-tecnica-modernizacion-modulos-4@57:41, charla-tecnica-modernizacion-modulos-4@58:08, charla-tecnica-modernizacion-modulos-4@59:05, charla-tecnica-modernizacion-modulos-4@1:00:01, charla-tecnica-modernizacion-modulos-4@1:00:22, charla-tecnica-modernizacion-modulos-4@1:06:19, charla-tecnica-modernizacion-modulos-4@1:11:34, charla-tecnica-modernizacion-modulos-4@1:13:36, charla-tecnica-modernizacion-modulos-4@1:04:30, charla-tecnica-modernizacion-modulos-4@1:07:43, charla-tecnica-modernizacion-modulos-4@1:03:08, charla-tecnica-modernizacion-modulos-4@1:18:28, charla-tecnica-modernizacion-modulos-4@1:37:41]
ultima_fuente: 2026-04-23
contradicciones: 0
---

# Descriptivo y POST-QUERY

## Definición
Un descriptivo es el campo que va al lado del código y muestra su descripción (por ejemplo, "desc lista pro" al lado de lista pro) [Charla 4 · 10:43](../charla-tecnica-modernizacion-modulos-4.md). Al generar un campo descriptivo siempre se indica la tabla a la que pertenece y el nombre del campo de descripción, para que el join se arme solo y después se complete [Charla 4 · 56:48](../charla-tecnica-modernizacion-modulos-4.md) [Charla 4 · 57:12](../charla-tecnica-modernizacion-modulos-4.md).

En Forms, los descriptivos de datos ya grabados se traen en el POST-QUERY, donde se llenan los campos al consultar; si existe el descriptivo, es obligatorio tenerlo en el POST-QUERY [Charla 6 · 27:31](../charla-tecnica-modernizacion-modulos-6.md). Cuando se hace una LOV con descripción, después hay que buscar el dato y llenarlo en el post-query [Charla 4 · 6:29](../charla-tecnica-modernizacion-modulos-4.md). La propiedad Column Mapping de la LOV indica qué valor va a qué campo: el código al campo código y la descripción al descriptivo [Charla 4 · 6:02](../charla-tecnica-modernizacion-modulos-4.md) [Charla 4 · 7:23](../charla-tecnica-modernizacion-modulos-4.md).

## Detalle
- **Caso del descriptivo vacío:** el descriptivo de esquema no traía datos porque quien dio de alta el campo se olvidó de cargarlo en el post-query; al consultar desde Forms se llenaban todos los campos menos ese [Charla 4 · 7:52](../charla-tecnica-modernizacion-modulos-4.md). En los otros campos que tenían Ref Code sí se llenaba en el post-query [Charla 4 · 6:53](../charla-tecnica-modernizacion-modulos-4.md).
- **Dónde está el código en Forms:** en un ítem descriptivo la LOV no está en el propio ítem, sino en el campo código anterior [Charla 4 · 3:14](../charla-tecnica-modernizacion-modulos-4.md). El ítem de destino del descriptivo de esquema se leyó como `DESP_ESQUEMA` (sin confirmar) [Charla 4 · 7:23](../charla-tecnica-modernizacion-modulos-4.md).
- **POST-QUERY vs alta:** en el POST-QUERY se trae lo que ya está en la base (ya tengo el código y traigo el nombre); al insertar el usuario carga el código y hay que traerle el nombre al costado [Charla 6 · 27:07](../charla-tecnica-modernizacion-modulos-6.md). Al insertar todo está vacío: se da la lista de valores y se agrega la descripción al elegir, o el validador del campo llena el otro campo [Charla 6 · 28:01](../charla-tecnica-modernizacion-modulos-6.md). Por eso un dato que se carga en el alta no va en el POST-QUERY [Charla 6 · 10:31](../charla-tecnica-modernizacion-modulos-6.md).
- **En la definición:** solo un descriptivo por tabla relacionada lleva la tabla; en el resto va null y se llenan después [Charla 4 · 9:19](../charla-tecnica-modernizacion-modulos-4.md) [Charla 4 · 9:45](../charla-tecnica-modernizacion-modulos-4.md). Los demás se llenan "como un post-query": un ítem se puede llenar en cualquier momento con el dato que se quiera [Charla 4 · 5:07](../charla-tecnica-modernizacion-modulos-4.md).
- **Completarlos en el paquete:** en el select, los campos que dicen null y el nombre del campo son los que faltan; se copia lo que está en el Forms, se hace el mismo select y el INTO al dato que corresponde [Charla 4 · 57:41](../charla-tecnica-modernizacion-modulos-4.md). Se copia el bloque completo BEGIN … EXCEPTION, para que si hay error quede nulo [Charla 4 · 58:08](../charla-tecnica-modernizacion-modulos-4.md), y se reemplazan las referencias con dos puntos del Forms por la variable del registro del paquete ("LR Move", sin confirmar) [Charla 4 · 59:05](../charla-tecnica-modernizacion-modulos-4.md).
- **Excepciones:** si no lo encuentra se asigna nulo; además debería estar TOO_MANY_ROWS, porque dominio más código no es clave primaria [Charla 4 · 1:00:01](../charla-tecnica-modernizacion-modulos-4.md) [Charla 4 · 1:00:22](../charla-tecnica-modernizacion-modulos-4.md).
- **Descriptivo que viene de un Record Group:** se toma uno de los bloques ya pegados (para mantener el BEGIN/EXCEPTION) y se le cambia el query [Charla 4 · 1:06:19](../charla-tecnica-modernizacion-modulos-4.md).
- **Asignar al type:** el valor se asigna campo por campo al type, que es el que devuelve el dato; cargarlo solo en una variable no alcanza y el descriptivo no se ve [Charla 4 · 1:11:34](../charla-tecnica-modernizacion-modulos-4.md) [Charla 4 · 1:13:36](../charla-tecnica-modernizacion-modulos-4.md).
- **Orden y campos nuevos:** el orden de los campos es tan importante como que estén todos [Charla 4 · 1:04:30](../charla-tecnica-modernizacion-modulos-4.md); un campo nuevo en la tabla también se agrega a mano en el paquete [Charla 4 · 1:07:43](../charla-tecnica-modernizacion-modulos-4.md).
- **Performance:** lo óptimo sería hacer el join de todos los descriptivos en el query, pero se hizo en el paquete porque queda más claro y representa cómo trabaja Forms [Charla 4 · 1:03:08](../charla-tecnica-modernizacion-modulos-4.md). Los descriptivos que se llenan aparte no se marcan campo query [Charla 4 · 1:18:28](../charla-tecnica-modernizacion-modulos-4.md).
- **Edición:** la descripción no se edita; se pone el código y la descripción se completa sola [Charla 4 · 1:37:41](../charla-tecnica-modernizacion-modulos-4.md).

## Contradicciones
Sin contradicciones entre las fuentes. La Charla 4 muestra un descriptivo roto por no estar en el post-query [Charla 4 · 7:52](../charla-tecnica-modernizacion-modulos-4.md) y la Charla 6 lo formula como obligación general [Charla 6 · 27:31](../charla-tecnica-modernizacion-modulos-6.md).

## Relacionados
- [Lista de valores](termino-lista-de-valores.md)
- [Una sola relación por tabla](caso-una-relacion-por-tabla.md)
- [Ref Code y Record Group](termino-ref-code-y-record-group.md)
- [Campo query](termino-campo-query.md)
- [Validador de campo](termino-validador-de-campo.md)

## Fuentes
| Video | Fecha | Minuto | Qué aporta |
|---|---|---|---|
| Charla 4 | 2026-04-02 | 3:14 – 9:45 | Descriptivo vacío por falta de post-query; Column Mapping; null en la definición |
| Charla 4 | 2026-04-02 | 56:48 – 1:13:36 | Join automático y completado de descriptivos en el paquete; asignación al type |
| Charla 6 | 2026-04-23 | 27:07 – 28:01 | POST-QUERY obligatorio para descriptivos; diferencia con el alta |
