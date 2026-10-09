# Plantilla y reglas para transcripciones procesadas

## Contexto del proyecto (para interpretar la jerga)

Proyecto "Modernización de módulos" (Tecnaris, sector seguros). Se migran pantallas/tablas de
Oracle Forms a un sistema nuevo parametrizable. Términos y probables errores de la
transcripción automática (ASR) ya identificados:

| Lo que dice el ASR | Probablemente es | Notas |
|---|---|---|
| "from", "fon", "Font", "fonk", "form", "Ford", "Fom", "Phone", "fam" | Forms / Oracle Forms (el form) | la pantalla vieja |
| "Red Code", "red Cow", "rescover", "res code" | casi siempre **Ref Code** (`CG_REF_CODES` [?]): tabla de códigos/dominios | valores fijos de un campo sin tabla propia |
| "record Group", "RG", "rector" (a veces) | Record Group (Oracle Forms) | su query alimenta la LOV |
| "Endesa", "desa" | en desa (desarrollo) | flujo desa → test → prod |
| "Love", "Lob", "logo" | LOV (lista de valores) | |
| "Post Chain", "poché", "postchet" | trigger POST-CHANGE | |
| "post Quei", "post Cueri", "Post Code" | trigger POST-QUERY | |
| "no data funk/phone/fan", "tu money rock" | NO_DATA_FOUND / TOO_MANY_ROWS | excepciones Oracle |
| "tai", "tripe", "taip", "list tail" | TYPE / list type | |
| "cuello", "cueri", "Wear", "intu" | query, WHERE, INTO | |
| "balidate", "validay", "validez" | validate (validador de campo) | |
| "Rambo", "polis", "police" | ramo / póliza | |
| "Jason", "J son", "JAS" | JSON | mensaje Front ↔ back |
| "trum", "Trump" (sobre fechas) | TRUNC | quita la hora; rompe índices |
| "Red Type", "reptile", "rectype" | rectype (tipo registro) | lo recibe el validador |
| "Live", "ivel" | label (título del campo) | |
| "mixer", "rapper", "lawer", "daite", "Day" | MIXED, UPPER, LOWER, DATE (Case Restriction) | |
| "Frank", "Franco", "foro" | Front | |
| "Column Mapy" | Column Mapping | propiedad de la LOV en Forms |
| "case restriction", "Apple mix", "mix", "APP" | propiedad Case Restriction: MIXED / UPPER | formato de varchar |
| "Prof" | Prod (producción) | ambientes: test → prod |
| "Pecs t origen recaudo", "Pex t origen recaudos", "Pex t recaudo" | tabla `?XT_ORIGEN_RECAUDO` (prefijo dudoso, ¿PXT?) | marcar [?] |
| "Pexen", "PXG", "PXGRE", "ese pen" | prefijo/esquema dudoso | marcar [?] |
| "parametría" | parametría / tablas de parametrización | término real |
| "grupo de negocio" | grupo de negocio | término real: link a otra pantalla |
| "ramo/póliza/certificado" | clave de póliza: ramo/póliza/certificado | término real de seguros |
| "PK", "varchar", "number", "null" | términos Oracle | |

Si un término no se puede resolver con confianza: dejá la mejor lectura y marcá `[?]`.
Si un fragmento es ininteligible: `[inaudible]`. NUNCA inventes contenido ni completes
con conocimiento general lo que no se dice.

## Formato de salida (Markdown con frontmatter OKF)

```markdown
---
type: Fuente de video
title: <título legible>
description: <1–2 frases: de qué trata>
resource: "Transcripciones/<nombre exacto del .docx>"
timestamp: <AAAA-MM-DD si se conoce, si no omitir>
duracion: "<h:mm:ss aprox, según último timestamp>"
participantes: [<nombres si aparecen; si no, []>]
dominio: <funcional | tecnico | ambos>
tags: [modernizacion-de-modulos, ...]
estado: borrador
calidad_transcripcion: <alta | media | baja>
---

# <título>

## Resumen
<5–10 bullets con lo que efectivamente se explicó/decidió>

## Temas
| # | Tema | Desde | Hasta | Dominio |
|---|---|---|---|---|
| 1 | ... | 0:02 | 7:45 | tecnico |

## Transcripción limpia por tema

### 1. <Tema> (0:02 – 7:45)
<Prosa limpia, fiel al original, en 3ra persona o discurso directo editado.
Quitar muletillas, repeticiones, charla irrelevante (mouse, "aguantame", etc.).
Conservar TODOS los datos: nombres de tablas, campos, reglas, pasos, números, tickets.
Insertar el timestamp de origen entre corchetes al inicio de cada idea: [14:59].
Si hay hablantes identificados: **Nombre:** ...>

> **Regla:** <cuando se enuncie una regla/obligación explícita, destacarla así>
> **Caso especial:** <excepciones, "hay un caso muy especial...">

## Términos detectados
| Término | Variante en el audio | Qué significa según el video | Timestamp |
|---|---|---|---|

## Reglas y casos especiales detectados
- [mm:ss] <regla o caso, una línea>

## Pendientes / dudas abiertas
- [mm:ss] <preguntas sin respuesta, cosas a confirmar, términos [?]>
```

Criterios de dominio: **funcional** = qué hace el negocio/usuario (pólizas, ramos,
pantallas de consulta, qué ve el usuario). **técnico** = tablas, campos, permisos,
scripts, Forms, migración, tipos de datos.
