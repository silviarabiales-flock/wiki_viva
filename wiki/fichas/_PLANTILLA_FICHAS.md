# Plantilla y reglas de las fichas consolidadas

Las fichas reúnen en un solo documento OKF lo que se dijo sobre un concepto en **todos** los videos.
Viven en `wiki/fichas/` y se enlazan desde `wiki/index.md`.

## Fuentes y nombres cortos

| Nombre corto | Archivo (desde `fichas/`) | Fecha |
|---|---|---|
| Charla 4 | `../charla-tecnica-modernizacion-modulos-4.md` | 2026-04-02 |
| Charla 6 | `../charla-tecnica-modernizacion-modulos-6.md` | 2026-04-23 |
| Capacitación | `../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md` | 2026-05-12 |
| Revisión | `../modernizacion-modulos-revision-avance-2026-06-16.md` | 2026-06-16 |

## Reglas

1. Solo se usa lo que está escrito en los documentos de video. Nada de conocimiento general.
2. **Cada afirmación termina con su cita**, con este formato exacto de link Markdown:
   `[Charla 4 · 16:39](../charla-tecnica-modernizacion-modulos-4.md)`
   El minuto va tal cual aparece en el documento de origen (`m:ss` o `h:mm:ss`) y tiene que existir en ese documento.
3. No se cita la sección "Pendientes / dudas abiertas". Los términos con `[?]` se mencionan como "sin confirmar".
4. **Contradicciones:**
   - Si una de las fuentes en conflicto es la **Charla 6**, prevalece la Charla 6 (regla del piloto).
   - Si no, prevalece la fuente más reciente y la contradicción queda "a confirmar".
   - Lo anterior no se borra: queda como versión previa con su cita.
5. Estado inicial `borrador`. `valida` indica quién tiene que validarla.

## Formato

```markdown
---
type: Término | Regla de negocio | Caso especial
title: <nombre>
description: <una frase>
aliases: [<sinónimos y cómo suena en el audio>]
dominio: funcional | tecnico | ambos
tags: [<etiquetas>]
estado: borrador
valida: referente funcional | referente técnico | ambos
fuentes: [<archivo-sin-.md>@<m:ss>, ...]
ultima_fuente: <AAAA-MM-DD>
contradicciones: <número>
---

# <nombre>

## Definición            (Término)  | ## Regla (Regla de negocio) | ## Situación (Caso especial)
<1 a 3 párrafos consolidados; cada oración con su cita>

## Detalle               (Término: uso y ejemplos · Regla: cuándo aplica y excepciones · Caso: qué hacer y riesgos)
- <punto> [Fuente · m:ss](../archivo.md)

## Contradicciones
> ⚠ **Contradicción:** [Charla 4 · x](...) decía …; [Charla 6 · y](...) dice … **Vigente: Charla 6** (ante contradicción prevalece la Charla 6).
(o "Sin contradicciones entre las fuentes.")

## Relacionados
- [<Otra ficha>](<otra-ficha>.md)

## Fuentes
| Video | Fecha | Minuto | Qué aporta |
|---|---|---|---|
```
