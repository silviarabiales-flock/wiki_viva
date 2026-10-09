---
type: Caso especial
title: Fecha con hora
description: Cuando la fecha guardada tiene hora, filtrar con TRUNC sobre la columna rompe el índice; lo correcto es ">= desde y < hasta + 1", y la solución provisoria saca el campo del query.
aliases: [fecha con hora, TRUNC, "trum", "Trump", "round", ">= desde y < hasta + 1", campo fuera del query, no campo query]
dominio: tecnico
tags: [campo-fecha, trunc, indices, performance, campo-query, filtro, operatoria, timeout, valor-compuesto]
estado: borrador
valida: referente técnico
fuentes: [capacitacion-validacion-compuesta-campo-fecha-2026-05-12@30:24, capacitacion-validacion-compuesta-campo-fecha-2026-05-12@39:04, capacitacion-validacion-compuesta-campo-fecha-2026-05-12@33:46, capacitacion-validacion-compuesta-campo-fecha-2026-05-12@35:13, capacitacion-validacion-compuesta-campo-fecha-2026-05-12@36:30, charla-tecnica-modernizacion-modulos-4@1:19:26]
ultima_fuente: 2026-05-12
contradicciones: 0
---

# Fecha con hora

## Situación
En el caso del log, el campo fecha tiene hora y el Forms le aplica TRUNC; con "fecha hasta" sin truncar no entran los registros con minutos y segundos de ese mismo día [Capacitación · 30:24](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). El Front arma "fecha entre X e Y" y no sabe que la fecha tiene hora [Capacitación · 31:21](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).

Aplicar TRUNC sobre la columna rompe el índice; con índice por fecha lo correcto es filtrar con `fecha >= fecha_desde AND fecha < fecha_hasta + 1` [Capacitación · 39:04](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).

## Detalle
- **Por qué "< hasta + 1":** el "menor estricto que hasta + 1" incluye todo el último día hasta las 23:59:59; con "<= fecha hasta" solo entran los del último día a las 0:00 y quedan afuera los de las 10, 11 o 12 horas [Capacitación · 39:04](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- **Alternativas planteadas** para "engañar" al Front, que solo maneja un campo: concatenar la hora 00:00 en el select, o crear otro campo ("fecha WHERE") que no sea campo de la tabla [Capacitación · 32:17](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- **Solución aplicada (provisoria):** en el select se devuelve TRUNC(fecha) con el alias del campo fecha, y el campo fecha se marca como no parte del query; así la base filtra por los demás campos y el Front filtra por la fecha cuando recibe los datos [Capacitación · 33:46](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- **Campo fuera del query:** si un campo es parte del query, el filtro va al WHERE de la base; si no, se ejecuta el query con el resto de los filtros y ese campo se filtra al recibir los datos, lo que es poco performante [Capacitación · 35:13](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). Coincide con la Charla 4: si el campo no está en el query hay que ejecutar todo y recién después ordenar [Charla 4 · 1:17:07](../charla-tecnica-modernizacion-modulos-4.md), y siempre hay que tratar de llevar todo lo posible al query [Charla 4 · 1:19:26](../charla-tecnica-modernizacion-modulos-4.md).
- En este caso hay bastantes otros filtros, así que podría andar bien; si tarda mucho, habrá que buscar otra manera [Capacitación · 35:42](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). Lo que no se puede es que la base aplique el TRUNC por nosotros [Capacitación · 36:11](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- **Riesgo de timeout:** la tabla tiene muchísimos registros y con algunos rangos de días el Front llega al timeout [Capacitación · 36:30](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- **Operatorias por rango:** hay que ver cómo usa el negocio la tabla; una opción es armar dos operatorias, una de últimos 30 días y otra para rangos más largos [Capacitación · 37:03](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- Con TRUNC no se usa el índice por fecha, igual que en el Forms: la solución provisoria funciona pero no es la mejor, y lo ideal es un índice por fecha con ">= desde, < hasta + 1" [Capacitación · 37:31](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- **Cómo marcarlo:** se indica en la definición de campos de la tabla, con el indicador de campo en query en N; aunque el campo pertenece a la tabla, al transformarlo con TRUNC ya no se puede filtrar en la base [Capacitación · 40:48](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). El nombre de esa tabla de definición ("FD campo actualización") está sin confirmar [Capacitación · 40:48](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- El Case Restriction de una fecha es DATE, y si se la quiere ver con hora hay una variante con hora cuyo valor exacto está sin confirmar [Capacitación · 41:43](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- Es un caso muy particular: para una fecha común, desde/hasta queda en el query y es mucho más performante [Capacitación · 43:42](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- La tarea del caso incluye marcar el campo fecha como no campo query, porque se lo transforma [Capacitación · 44:38](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).

## Contradicciones
Sin contradicciones entre las fuentes.

## Relacionados
- [Valor compuesto](termino-valor-compuesto.md)
- [Campo query](termino-campo-query.md)
- [Case Restriction](termino-case-restriction.md)
- [Validador de campo](termino-validador-de-campo.md)

## Fuentes
| Video | Fecha | Minuto | Qué aporta |
|---|---|---|---|
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 1:17:07, 1:19:26 | Lo que no está en el query se ordena/filtra después; llevar todo lo posible al query |
| [Capacitación](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md) | 2026-05-12 | 30:24, 31:21, 39:04 | TRUNC del Forms, rotura del índice y ">= desde y < hasta + 1" |
| [Capacitación](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md) | 2026-05-12 | 32:17, 33:46, 35:13, 35:42, 36:11 | Alternativas y solución provisoria con campo fuera del query |
| [Capacitación](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md) | 2026-05-12 | 36:30, 37:03, 37:31 | Timeouts y operatorias por rango |
| [Capacitación](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md) | 2026-05-12 | 40:48, 41:43, 43:42, 44:38 | Cómo marcar el campo como no query; DATE; tarea |
