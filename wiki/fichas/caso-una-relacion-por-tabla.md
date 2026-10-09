---
type: Caso especial
title: Una sola relación por tabla
description: El proceso generador relaciona cada tabla una sola vez; si varios campos apuntan a la misma tabla (monedas, Ref Code), uno lleva la relación automática y los demás descriptivos se completan en el paquete.
aliases: [una relación por tabla, relación única, "la Red Code puede ir una sola vez", moneda dos, CG_REF_CODES 2 (sin confirmar)]
dominio: tecnico
tags: [modernizacion-de-modulos, generador, relaciones, join, ref-code, monedas, descriptivos, paquete, definicion-de-campos]
estado: borrador
valida: referente técnico
fuentes: [charla-tecnica-modernizacion-modulos-4@4:11, charla-tecnica-modernizacion-modulos-4@4:41, charla-tecnica-modernizacion-modulos-4@10:14, charla-tecnica-modernizacion-modulos-4@9:45, charla-tecnica-modernizacion-modulos-4@9:19, charla-tecnica-modernizacion-modulos-4@10:43, charla-tecnica-modernizacion-modulos-4@5:07, charla-tecnica-modernizacion-modulos-4@53:20, charla-tecnica-modernizacion-modulos-4@55:57, charla-tecnica-modernizacion-modulos-4@56:22, charla-tecnica-modernizacion-modulos-4@57:41, charla-tecnica-modernizacion-modulos-4@58:08, charla-tecnica-modernizacion-modulos-4@1:15:09, charla-tecnica-modernizacion-modulos-4@1:15:38, charla-tecnica-modernizacion-modulos-4@1:16:09, charla-tecnica-modernizacion-modulos-4@1:16:38, charla-tecnica-modernizacion-modulos-4@1:19:26, charla-tecnica-modernizacion-modulos-4@1:18:00, charla-tecnica-modernizacion-modulos-4@1:00:22, charla-tecnica-modernizacion-modulos-4@1:13:36, charla-tecnica-modernizacion-modulos-4@1:21]
ultima_fuente: 2026-04-02
contradicciones: 0
---

# Una sola relación por tabla

## Situación
El proceso no puede hacer relaciones sobre la misma tabla varias veces [Charla 4 · 4:11](../charla-tecnica-modernizacion-modulos-4.md). Si el campo moneda se relaciona con la tabla de monedas para obtener la descripción y hay otro campo "moneda dos" que también se relaciona con esa tabla, eso no se puede hacer desde el script: de movida solo puede haber una relación por tabla y lo demás se ajusta a mano [Charla 4 · 4:41](../charla-tecnica-modernizacion-modulos-4.md).

Pasa mucho con la Ref Code, porque todo campo con distintos valores fijos va a esa tabla [Charla 4 · 10:14](../charla-tecnica-modernizacion-modulos-4.md). Si hay más de un campo con Ref Code, hay que seleccionar uno solo para hacer la relación [Charla 4 · 4:41](../charla-tecnica-modernizacion-modulos-4.md); cuando el proceso detecta que ya se hizo una relación con esa tabla, no arma otra [Charla 4 · 9:45](../charla-tecnica-modernizacion-modulos-4.md).

## Detalle
- **Qué hacer en la definición:** elegir un solo campo y ponerle la tabla Ref Code; en el resto va null, igual que en otros descriptivos [Charla 4 · 9:19](../charla-tecnica-modernizacion-modulos-4.md). En el ejemplo de la Charla 4 había 6 campos a agregar, los 6 de la Ref Code, y solo a uno se le puso la tabla [Charla 4 · 10:43](../charla-tecnica-modernizacion-modulos-4.md).
- **Los demás descriptivos se llenan después,** como un post-query: un ítem se puede llenar en cualquier momento con el dato que se quiera [Charla 4 · 5:07](../charla-tecnica-modernizacion-modulos-4.md).
- **Dos maneras de completarlos en el paquete:** ponerlos en el FROM, que implica cambiarlo y es bastante complejo, o copiar los códigos de las Ref Codes y ponerlos abajo [Charla 4 · 53:20](../charla-tecnica-modernizacion-modulos-4.md). Para una segunda relación en el FROM habría que copiar el bloque de `CG_REF_CODES`, ponerle "CG_REF_CODES 2" y agregarlo, una vez por cada descripción; no se justifica [Charla 4 · 55:57](../charla-tecnica-modernizacion-modulos-4.md).
- **Opción elegida:** con una misma tabla se elige una sola relación y las otras se cargan a mano [Charla 4 · 56:22](../charla-tecnica-modernizacion-modulos-4.md), copiando del Forms el mismo select con su INTO y el bloque BEGIN … EXCEPTION [Charla 4 · 57:41](../charla-tecnica-modernizacion-modulos-4.md) [Charla 4 · 58:08](../charla-tecnica-modernizacion-modulos-4.md).
- **Tablas distintas no tienen el problema:** si en la definición hay otra tabla, aparece otro join en el FROM con el nombre de esa tabla (como en el ejemplo de monedas) [Charla 4 · 56:22](../charla-tecnica-modernizacion-modulos-4.md).
- **Verificación:** la relación generada sola por el proceso anduvo; con 3 o 4 tablas relacionadas hay que revisarlo porque se complica [Charla 4 · 1:15:09](../charla-tecnica-modernizacion-modulos-4.md) [Charla 4 · 1:15:38](../charla-tecnica-modernizacion-modulos-4.md).
- **Riesgo de performance:** armar todo en el FROM con la Ref Code varias veces (alias 1, 2, 3) se vuelve un lío; sería más performante en el query, pero en una tabla chica la solución en el paquete funciona [Charla 4 · 1:16:09](../charla-tecnica-modernizacion-modulos-4.md) [Charla 4 · 1:16:38](../charla-tecnica-modernizacion-modulos-4.md).
- **Riesgo en orden y filtro:** solo el descriptivo que vino por join se marca campo query; los completados en el paquete no, así que no se pueden ordenar ni filtrar en la base [Charla 4 · 1:19:26](../charla-tecnica-modernizacion-modulos-4.md) [Charla 4 · 1:18:00](../charla-tecnica-modernizacion-modulos-4.md).
- **Riesgo de datos:** los bloques copiados deberían manejar NO_DATA_FOUND y TOO_MANY_ROWS, porque dominio más código no es clave primaria [Charla 4 · 1:00:22](../charla-tecnica-modernizacion-modulos-4.md); y el valor tiene que asignarse al type, no solo a una variable [Charla 4 · 1:13:36](../charla-tecnica-modernizacion-modulos-4.md).
- **Permisos:** igual hay que dar permisos a todas las tablas relacionadas, porque el script de relación los necesita [Charla 4 · 1:21](../charla-tecnica-modernizacion-modulos-4.md).

## Contradicciones
Sin contradicciones entre las fuentes. El caso solo se trata en la Charla 4.

## Relacionados
- [Ref Code y Record Group](termino-ref-code-y-record-group.md)
- [Descriptivo y POST-QUERY](termino-descriptivo-y-post-query.md)
- [Campo query](termino-campo-query.md)
- [Permisos sobre tablas relacionadas](regla-permisos-tablas-relacionadas.md)

## Fuentes
| Video | Fecha | Minuto | Qué aporta |
|---|---|---|---|
| Charla 4 | 2026-04-02 | 4:11 – 5:07 | Restricción del generador y elección de un solo campo |
| Charla 4 | 2026-04-02 | 8:50 – 10:43 | Ref Code una vez por definición; null en los demás |
| Charla 4 | 2026-04-02 | 53:20 – 58:08 | Cómo completar las demás relaciones en el paquete |
| Charla 4 | 2026-04-02 | 1:15:09 – 1:19:26 | Verificación, performance y campo query |
