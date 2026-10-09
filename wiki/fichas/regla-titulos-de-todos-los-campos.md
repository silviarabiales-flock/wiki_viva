---
type: Regla de negocio
title: Títulos de todos los campos
description: Hay que completar el título (label) de todos los campos, como se ven en el Forms, lo antes posible y en la definición, porque después se copia a operatorias, edit e insert.
aliases: [label, "Live", "ivel", títulos por defecto]
dominio: ambos
tags: [titulos, label, definicion-de-campos, parametrizacion, forms]
estado: borrador
valida: ambos
fuentes: [charla-tecnica-modernizacion-modulos-4@12:33, charla-tecnica-modernizacion-modulos-4@13:02, charla-tecnica-modernizacion-modulos-4@29:33, charla-tecnica-modernizacion-modulos-4@30:01, charla-tecnica-modernizacion-modulos-4@30:31, charla-tecnica-modernizacion-modulos-4@31:26, charla-tecnica-modernizacion-modulos-4@32:23, charla-tecnica-modernizacion-modulos-4@33:56, charla-tecnica-modernizacion-modulos-4@35:21, charla-tecnica-modernizacion-modulos-4@36:40, charla-tecnica-modernizacion-modulos-4@37:46, capacitacion-validacion-compuesta-campo-fecha-2026-05-12@43:42, capacitacion-validacion-compuesta-campo-fecha-2026-05-12@44:09, capacitacion-validacion-compuesta-campo-fecha-2026-05-12@44:38]
ultima_fuente: 2026-05-12
contradicciones: 0
---

# Títulos de todos los campos

## Regla
Hay que completar los títulos (label) de todos los campos, como se ven en el Forms, para que el usuario los reconozca; conviene hacerlo lo antes posible, aunque el campo no se muestre (ID, IP, subsistema, usuario), porque al generar después una operatoria, un edit o un insert el proceso copia el label automáticamente [Capacitación · 43:42](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).

Es más sencillo cargar los títulos en la definición, así ya se crea bien; si se hace después desde la pantalla de parametrización, hay que hacerlo para el insert, para el update y para lo demás [Charla 4 · 30:01](../charla-tecnica-modernizacion-modulos-4.md).

## Detalle
- **Cuándo:** al insertar un campo nuevo en la definición se completan la tabla, el nombre y el título [Charla 4 · 12:33](../charla-tecnica-modernizacion-modulos-4.md); si no, se deja en null y después se cargan todos juntos [Charla 4 · 13:02](../charla-tecnica-modernizacion-modulos-4.md). Con todos los campos cargados, falta poner los títulos por defecto [Charla 4 · 29:33](../charla-tecnica-modernizacion-modulos-4.md). Completar los títulos por defecto figura en la tarea de la Capacitación [Capacitación · 44:38](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- **Dónde:** en la pantalla de parametrización (FDQM70000, sin confirmar) aparecen los campos de la definición [Charla 4 · 30:31](../charla-tecnica-modernizacion-modulos-4.md), y en la parte de abajo es más fácil cargar los títulos [Charla 4 · 31:26](../charla-tecnica-modernizacion-modulos-4.md).
- **Qué texto:** mirando la pantalla vieja, el título tiene que reflejar más o menos lo mismo (por ejemplo, "Código") [Charla 4 · 31:26](../charla-tecnica-modernizacion-modulos-4.md). El label es el título del campo [Capacitación · 44:09](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- **Ajustes permitidos:** si en el Forms el título está en dos renglones, acá no hay dos renglones [Charla 4 · 32:23](../charla-tecnica-modernizacion-modulos-4.md). Si el campo no aparece en la pantalla vieja, se le pone un título corto solo para saber qué es (por ejemplo, "sigla nav") [Charla 4 · 33:56](../charla-tecnica-modernizacion-modulos-4.md). Se puede variar el texto para que no se choque con otro (por ejemplo, "desc productor", "desc caja") [Charla 4 · 36:40](../charla-tecnica-modernizacion-modulos-4.md).
- **Excepción (layout):** se respetan los títulos, pero no la disposición del Forms: en el sistema nuevo todo es una grilla y cada campo es una columna; las vistas definen cuántos campos se ven [Charla 4 · 35:21](../charla-tecnica-modernizacion-modulos-4.md).
- **Por qué vale la pena:** aunque parezca tedioso, con esta carga ya se está preparando el frontend (qué se va a ver) y armando las distintas capas [Charla 4 · 37:46](../charla-tecnica-modernizacion-modulos-4.md).

## Contradicciones
Sin contradicciones entre las fuentes.

## Relacionados
- [Término: Case Restriction](termino-case-restriction.md)
- [Término: campo query](termino-campo-query.md)
- [Regla: pase entre ambientes](regla-pase-entre-ambientes.md)

## Fuentes
| Video | Fecha | Minuto | Qué aporta |
|---|---|---|---|
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 12:33 | El título se completa al insertar el campo |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 13:02 | Si no, null y luego todos juntos |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 29:33 | Faltan los títulos por defecto |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 30:01 | Más sencillo en la definición que en insert/update |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 30:31 | Pantalla de parametrización FDQM70000 |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 31:26 | Dónde cargarlos; reflejar la pantalla vieja |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 32:23 | No hay títulos en dos renglones |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 33:56 | Título corto para campos que no se ven en Forms |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 35:21 | No se replica el layout del Forms |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 36:40 | Títulos ajustados para que no se choquen |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 37:46 | Se prepara el frontend |
| [Capacitación](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md) | 2026-05-12 | 43:42 | Regla: label de todos los campos, como en el Forms |
| [Capacitación](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md) | 2026-05-12 | 44:09 | Label = título del campo |
| [Capacitación](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md) | 2026-05-12 | 44:38 | Tarea: completar títulos por defecto |
