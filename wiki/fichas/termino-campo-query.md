---
type: Término
title: Campo query (parte del query)
description: Indicador de la definición de campos que marca si el campo está en el select del query; define si el orden y el filtro los resuelve la base o se hacen después de traer los datos.
aliases: [campo query, "en cueri", "in campo query", campo en query, parte del query, no campo query, indicador de campo query]
dominio: tecnico
tags: [modernizacion-de-modulos, campo-query, performance, orden, filtro, definicion-de-campos, join, descriptivos, front]
estado: borrador
valida: referente técnico
fuentes: [charla-tecnica-modernizacion-modulos-4@1:16:38, charla-tecnica-modernizacion-modulos-4@1:18:28, charla-tecnica-modernizacion-modulos-4@1:17:37, capacitacion-validacion-compuesta-campo-fecha-2026-05-12@35:13, charla-tecnica-modernizacion-modulos-4@1:17:07, charla-tecnica-modernizacion-modulos-4@1:18:00, charla-tecnica-modernizacion-modulos-4@1:19:26, charla-tecnica-modernizacion-modulos-4@1:18:56, charla-tecnica-modernizacion-modulos-4@1:20:27, charla-tecnica-modernizacion-modulos-4@1:20:55, charla-tecnica-modernizacion-modulos-4@1:16:09, capacitacion-validacion-compuesta-campo-fecha-2026-05-12@33:46, capacitacion-validacion-compuesta-campo-fecha-2026-05-12@40:48, capacitacion-validacion-compuesta-campo-fecha-2026-05-12@35:42, capacitacion-validacion-compuesta-campo-fecha-2026-05-12@43:42]
ultima_fuente: 2026-05-12
contradicciones: 0
---

# Campo query (parte del query)

## Definición
En la definición de tablas hay un campo que indica si cada campo está en el query o no [Charla 4 · 1:16:38](../charla-tecnica-modernizacion-modulos-4.md). Se marca "campo query" a los campos que están en el select del query, incluidos los que vienen por join; a los descriptivos que se llenan aparte en el paquete no se les marca [Charla 4 · 1:18:28](../charla-tecnica-modernizacion-modulos-4.md).

El indicador existe para mejorar la performance [Charla 4 · 1:17:37](../charla-tecnica-modernizacion-modulos-4.md). Si un campo está marcado como parte del query, el filtro va al WHERE de la base; si no lo está, se ejecuta el query con el resto de los filtros y el filtrado por ese campo se hace al recibir los datos, lo que es poco performante [Capacitación · 35:13](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).

## Detalle
- **Orden desde el Front:** si el campo está en el query, se manda el texto del query con el ORDER BY y lo resuelve la base, mucho más performante porque el dato llega ya ordenado; si no está (se llena aparte en el paquete), hay que ejecutar todo y recién después ordenar [Charla 4 · 1:17:07](../charla-tecnica-modernizacion-modulos-4.md).
- **Qué se puede ordenar y filtrar en la base:** todo lo que está en el query (por ejemplo ORDER BY origen, descripción, productor); lo que en el select figura como null y se llena después no se puede ordenar ni filtrar así [Charla 4 · 1:18:00](../charla-tecnica-modernizacion-modulos-4.md).
- **Regla de diseño:** siempre hay que tratar de llevar todo lo posible al query, porque es muy importante para la performance del Front [Charla 4 · 1:19:26](../charla-tecnica-modernizacion-modulos-4.md) [Capacitación · 35:13](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- **Ejemplo con join:** si la descripción de la moneda se trae con un join en el query, se marca campo query; si se busca abajo en el paquete, no, y es menos performante [Charla 4 · 1:18:56](../charla-tecnica-modernizacion-modulos-4.md). En la tabla de la Charla 4 solo se marcó el primer descriptivo (descripción de lista pro), que vino por join [Charla 4 · 1:19:26](../charla-tecnica-modernizacion-modulos-4.md).
- **Qué conviene llevar al query:** normalmente, si hay un join y el dato tiene primary key, se puede llevar al query; si es complejo, se saca [Charla 4 · 1:20:27](../charla-tecnica-modernizacion-modulos-4.md). Lo habitual (producto-descripción, banco-descripción) se puede poner en el query [Charla 4 · 1:20:55](../charla-tecnica-modernizacion-modulos-4.md).
- **Por qué a veces no se lleva todo:** armar todo en el FROM con la Ref Code varias veces (alias 1, 2, 3) se vuelve un lío; sería más performante, pero en una tabla chica la solución de llenar en el paquete funciona [Charla 4 · 1:16:09](../charla-tecnica-modernizacion-modulos-4.md) [Charla 4 · 1:16:38](../charla-tecnica-modernizacion-modulos-4.md).
- **Cuándo poner N aunque el campo sea de la tabla:** en el caso de la fecha con hora se devuelve TRUNC(fecha) en el select con el alias del campo fecha y se marca el campo como no parte del query; así la base filtra por los demás campos y el Front filtra la fecha al recibir los datos [Capacitación · 33:46](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). Aunque el campo pertenece a la tabla, al transformarlo con TRUNC ya no se puede filtrar en la base [Capacitación · 40:48](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- **Dónde se marca:** en la definición de campos de la tabla ("FD campo actualización", nombre sin confirmar), con el indicador de campo en query ("in campo query") en N [Capacitación · 40:48](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). La transcripción agrega que también se puede modificar desde el "Record Group" ("rector", lectura del audio sin confirmar) o entrando a la tabla [Capacitación · 40:48](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md); ver la nota de interpretación en [Ref Code y Record Group](termino-ref-code-y-record-group.md).
- **Riesgo de performance:** la solución con N funciona si hay bastantes otros filtros; si tarda mucho habrá que buscar otra manera [Capacitación · 35:42](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). Para una fecha común, el filtro desde/hasta queda en el query y es mucho más performante [Capacitación · 43:42](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).

## Contradicciones
Sin contradicciones entre las fuentes. La Charla 4 indica marcar campo query a lo que está en el select [Charla 4 · 1:18:28](../charla-tecnica-modernizacion-modulos-4.md) y la Capacitación marca N a un campo que está en el select pero transformado con TRUNC [Capacitación · 40:48](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md): es una excepción justificada en la propia fuente (no se puede filtrar en la base), no una afirmación incompatible. Ambas coinciden en llevar todo lo posible al query [Charla 4 · 1:19:26](../charla-tecnica-modernizacion-modulos-4.md) [Capacitación · 35:13](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).

## Relacionados
- [Descriptivo y POST-QUERY](termino-descriptivo-y-post-query.md)
- [Una sola relación por tabla](caso-una-relacion-por-tabla.md)
- [Fecha con hora](caso-fecha-con-hora.md)
- [Valor compuesto](termino-valor-compuesto.md)
- [Case Restriction](termino-case-restriction.md)

## Fuentes
| Video | Fecha | Minuto | Qué aporta |
|---|---|---|---|
| Charla 4 | 2026-04-02 | 1:16:09 – 1:20:55 | Qué es el indicador, efecto en orden y filtro, performance, ejemplos con join |
| Capacitación | 2026-05-12 | 33:46 – 35:42 | Campo fuera del query: filtrado al recibir los datos; poco performante |
| Capacitación | 2026-05-12 | 40:48, 43:42 | Cuándo y dónde poner N (fecha transformada con TRUNC) |
