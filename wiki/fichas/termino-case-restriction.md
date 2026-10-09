---
type: Término
title: Case Restriction (formato del campo)
description: Propiedad de la definición de campos que, además de mayúsculas/minúsculas, indica el formato con que el Front muestra el dato (MONTO, NUMBER, UPPER, MIXED, LOWER, DATE).
aliases: [Case Restriction, case restriction, formato del campo, "Apple mix", "mix", "Apple", "APP", "mixer", "rapper", "lawer", "daite", "Day", "Dave", "van Amber" (NUMBER, sin confirmar), MONTO, NUMBER, UPPER, MIXED, LOWER, DATE]
dominio: tecnico
tags: [modernizacion-de-modulos, case-restriction, formato, monto, number, upper, mixed, lower, date, definicion-de-campos, front]
estado: borrador
valida: referente técnico
fuentes: [charla-tecnica-modernizacion-modulos-4@21:17, charla-tecnica-modernizacion-modulos-4@21:43, charla-tecnica-modernizacion-modulos-4@22:29, charla-tecnica-modernizacion-modulos-4@23:27, capacitacion-validacion-compuesta-campo-fecha-2026-05-12@41:43, charla-tecnica-modernizacion-modulos-4@22:04, charla-tecnica-modernizacion-modulos-4@22:59, charla-tecnica-modernizacion-modulos-4@23:57, charla-tecnica-modernizacion-modulos-4@24:22, charla-tecnica-modernizacion-modulos-4@20:49, charla-tecnica-modernizacion-modulos-4@25:30, charla-tecnica-modernizacion-modulos-4@25:53, charla-tecnica-modernizacion-modulos-4@44:57, charla-tecnica-modernizacion-modulos-4@30:31, charla-tecnica-modernizacion-modulos-4@45:28, capacitacion-validacion-compuesta-campo-fecha-2026-05-12@44:38]
ultima_fuente: 2026-05-12
contradicciones: 0
---

# Case Restriction (formato del campo)

## Definición
Case Restriction es el campo de la definición (el que en Forms muestra "mix") que en el sistema nuevo también se usa para indicar el formato del dato: para un varchar se puede poner MIXED y para un numérico que es monto se pone MONTO [Charla 4 · 21:17](../charla-tecnica-modernizacion-modulos-4.md). En numéricos va MONTO o NUMBER, siempre escrito en mayúsculas [Charla 4 · 21:43](../charla-tecnica-modernizacion-modulos-4.md). El Front interpreta MONTO como "esto es un monto" y le pone separación de miles y decimales, mientras que NUMBER es un entero sin separadores [Charla 4 · 22:29](../charla-tecnica-modernizacion-modulos-4.md).

El proceso genera un valor por defecto igual para todos los campos y hay que definirlo campo por campo [Charla 4 · 23:27](../charla-tecnica-modernizacion-modulos-4.md). Ese Case Restriction generado hay que corregirlo según el tipo de dato, porque si no las cosas dejan de funcionar: number lleva NUMBER o MONTO, varchar lleva MIXED, UPPER o LOWER, y date lleva DATE [Capacitación · 41:43](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).

## Detalle
- **Origen del uso como formato:** apareció cuando se empezó a dar formato a los montos, por eso el equipo todavía no lo conocía [Charla 4 · 22:04](../charla-tecnica-modernizacion-modulos-4.md). Había números que no son montos a los que les aparecían las comas [Charla 4 · 22:29](../charla-tecnica-modernizacion-modulos-4.md).
- **Ejemplo de por qué no todo número es MONTO:** el número de asiento (algo como 101020230102) se necesita tal cual; con una coma cada 3 dígitos se pierde [Charla 4 · 22:59](../charla-tecnica-modernizacion-modulos-4.md).
- **Criterio para number:** sin decimales (entero) → NUMBER; con decimales (dos, cuatro…) → MONTO [Charla 4 · 22:29](../charla-tecnica-modernizacion-modulos-4.md). Una PK numérica lleva NUMBER, no MONTO [Charla 4 · 23:27](../charla-tecnica-modernizacion-modulos-4.md). En la tabla de la Charla 4 (nivel de permiso, grupo recaudador, etc.) todos los numéricos son NUMBER porque no hay ningún monto [Charla 4 · 23:57](../charla-tecnica-modernizacion-modulos-4.md).
- **Caso especial (entero con separador de miles):** "ingresos mensuales" es entero y va NUMBER, pero si el usuario quiere que un entero muestre separador de miles (por ejemplo, porque es una cantidad muy grande) se le pone MONTO [Charla 4 · 24:22](../charla-tecnica-modernizacion-modulos-4.md).
- **Criterio para varchar:** un varchar puede llevar MIXED [Charla 4 · 20:49](../charla-tecnica-modernizacion-modulos-4.md); un varchar que es parte de la clave primaria lleva UPPER para que quede en mayúsculas, porque las claves tienen que aparecer sí o sí en mayúsculas [Charla 4 · 22:59](../charla-tecnica-modernizacion-modulos-4.md). La Capacitación agrega LOWER como opción para varchar [Capacitación · 41:43](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- **Criterio para date:** DATE; si se quiere ver con hora existe una variante con hora cuyo valor exacto está sin confirmar (el audio dice "day/Dave") [Capacitación · 41:43](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- **Mismos valores que en Forms:** se representaron igual que en Forms para que lo que se ve en Forms se pase sin conversión; en Forms la propiedad aparece como MIXED [Charla 4 · 25:30](../charla-tecnica-modernizacion-modulos-4.md) [Charla 4 · 25:53](../charla-tecnica-modernizacion-modulos-4.md).
- **Dónde se carga:** se actualiza en la definición una vez cargados todos los campos, y también se puede hacer desde la pantalla de parametrización [Charla 4 · 44:57](../charla-tecnica-modernizacion-modulos-4.md). En esa pantalla el Case Restriction tenía una lista de valores a la que hubo que agregarle los valores nuevos [Charla 4 · 30:31](../charla-tecnica-modernizacion-modulos-4.md); la lista todavía no tenía MONTO, pero se puede agregar en la Red Code (Ref Code) [Charla 4 · 45:28](../charla-tecnica-modernizacion-modulos-4.md).
- **Tarea típica:** al revisar una definición generada, corregir los tipos de Case Restriction junto con los títulos de los campos [Capacitación · 44:38](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).

## Contradicciones
Sin contradicciones entre las fuentes. La Charla 4 solo habla de numéricos (MONTO/NUMBER) y varchar (MIXED/UPPER) [Charla 4 · 21:43](../charla-tecnica-modernizacion-modulos-4.md) [Charla 4 · 22:59](../charla-tecnica-modernizacion-modulos-4.md); la Capacitación repite esos criterios y agrega LOWER y DATE [Capacitación · 41:43](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). La Charla 4 no dice nada sobre fechas, así que el valor DATE es un complemento y no una contradicción.

## Relacionados
- [Campo query](termino-campo-query.md)
- [Lista de valores](termino-lista-de-valores.md)
- [Ref Code y Record Group](termino-ref-code-y-record-group.md)
- [Títulos de todos los campos](regla-titulos-de-todos-los-campos.md)
- [Fecha con hora](caso-fecha-con-hora.md)

## Fuentes
| Video | Fecha | Minuto | Qué aporta |
|---|---|---|---|
| Charla 4 | 2026-04-02 | 20:49 – 25:53 | Case Restriction como formato; MONTO/NUMBER/UPPER/MIXED; motivo y casos |
| Charla 4 | 2026-04-02 | 30:31, 44:57, 45:28 | Carga desde la pantalla de parametrización y lista de valores del Case Restriction |
| Capacitación | 2026-05-12 | 41:43, 44:38 | Criterio completo por tipo: number, varchar (incluye LOWER) y date (DATE) |
