---
type: Fuente de video
title: "Modernización de módulos – Revisión de avance (16/06/2026)"
description: Explicación de cómo se arma un link a otra pantalla mediante "grupos de negocio" (póliza, productor, ingreso, etc.) y cómo pedir grupos nuevos; cierre con scripts pendientes de ejecutar.
resource: "Transcripciones/Modernización de módulos - Revision de avance 20260616.docx"
timestamp: 2026-06-16
duracion: "0:08:49"
participantes: [Martín Ocampo, Gustavo Ferreyra, Diego Salvatierra, Laura Benítez]
dominio: ambos
tags: [modernizacion-de-modulos, grupo-de-negocio, links, parametria, poliza, productor, ingreso]
estado: borrador
calidad_transcripcion: media
---

# Modernización de módulos – Revisión de avance (16/06/2026)

## Resumen

- Un **grupo de negocio** es la forma estándar de crear un campo que funciona como **link a otra pantalla** (por ejemplo, abrir la consulta de póliza desde una grilla).
- Para usarlo se agrega un **campo nuevo** (por convención "ver póliza", "ver productor") y se lo asocia en la parametría al grupo de negocio que corresponde.
- El grupo **póliza** recibe la clave concatenada **ramo/póliza/certificado**; el grupo **productor** recibe solo el número de productor (vía una función, sin concatenar).
- Grupos de negocio definidos hoy: **póliza, ingreso, cuenta corriente, productor, cliente, procesos manuales y póliza ART**.
- Los grupos se definen en una **función** (la última del listado del paquete); solo los agregan Gustavo/Martín, porque cada alta requiere hacer todos los pasajes.
- Si un link con parámetros no encaja en un grupo existente, hay que avisarles y ellos evalúan si corresponde **grupo de negocio, link o URL**.
- Diego compartió en el chat del grupo los scripts a ejecutar para avanzar con los tickets pendientes; queda una URL a agregar (ticket 4318).

## Temas

| # | Tema | Desde | Hasta | Dominio |
|---|---|---|---|---|
| 1 | Cómo funciona el link "ver póliza" con grupo de negocio | 0:18 | 2:39 | ambos |
| 2 | Grupos de negocio existentes y cómo pedir uno nuevo | 2:58 | 7:24 | ambos |
| 3 | Scripts pendientes y URL del ticket 4318 | 7:35 | 8:43 | tecnico |

## Transcripción limpia por tema

### 1. Cómo funciona el link "ver póliza" con grupo de negocio (0:18 – 2:39)

[0:05] Mientras Gustavo abre la parametría, Martín muestra el ejemplo.

**Martín Ocampo:** [0:18] Desde la pantalla, al hacer clic en el campo, se abre la póliza: se le manda como parámetro el número de póliza y el certificado. Eso se resuelve con un **grupo de negocio**. Para trabajarlo hay que **agregar un campo nuevo**; generalmente se le pone "ver póliza" (o "ver productor"), aunque es un nombre elegido por convención. En el ejemplo hay dos grupos de negocio armados (póliza y productor).

> **Regla:** [0:18] Al grupo de negocio póliza se le manda el valor concatenado **ramo + "/" + número de póliza + "/" + número de certificado**. En pantalla se muestra el campo "ver póliza".

[1:22] Al indicar en la parametría (la que muestra Gus) que el campo corresponde a un grupo de negocio, el sistema busca el link solo: todo está en tabla, ya linkeado.

[1:42] Los links habituales se arman siempre como grupo de negocio. Algunos ya están creados, como **productor**, que solo necesita el número de productor.

> **Regla:** [1:42] Aunque el valor sea único (por ejemplo, el productor), se arma **un campo nuevo** para el link; **no se usa el campo de la tabla** para linkear.

**Gustavo Ferreyra:** [2:12] En el caso de productor el valor se obtiene mediante una función, sin concatenar nada; trae solo el productor. [2:21] Le indica a Diego que mire la imagen que mandó del "campo de actualización": en el campo definido como grupo de negocio se pone "póliza" y el productor que corresponda.

### 2. Grupos de negocio existentes y cómo pedir uno nuevo (2:58 – 7:24)

**Diego Salvatierra:** [2:58] ¿Cómo se definen los grupos de negocio?

**Gustavo / Martín:** [3:04] Se definen en una **función** (no en un procedimiento): la última función del listado.

**Gustavo:** [3:12] Grupos de negocio definidos al momento:

- póliza
- ingreso
- cuenta corriente
- productor
- cliente
- procesos manuales
- póliza ART

> **Regla:** [3:12–3:48] Si un link con parámetros no corresponde a ninguno de esos grupos, **hay que avisarles** (Gustavo/Martín) y ellos lo agregan. No se modifica la función por cuenta propia: cada vez que se agrega algo hay que hacer todos los pasajes para que funcione. Ellos evalúan si corresponde **grupo de negocio, link o URL**.

[4:08] Si el link es de póliza, ingreso o cualquiera de los ya definidos, directamente se define como grupo de negocio: se crea un campo más y se siguen todos los pasos.

**Diego:** [4:20] ¿En la documentación [?] ("Buffet") está claro cómo se construye el link?

**Martín:** [4:26] Se puede tomar como modelo el ejemplo existente, que tiene póliza y productor.

[4:42–6:52] Buscan un ejemplo del grupo **ingreso**: Gustavo menciona la tabla "Pex t recaudo" [?] y un prefijo dudoso ("PXG / PXGRE", "Pexen") [?] que no logra confirmar. [5:38] Revisa la parametría y concluye que esa tabla no tiene ingreso.

**Martín:** [6:56] La clave del grupo ingreso se arma acumulando **esquema, compañía de ingreso y número de ingreso** (concatenado de esos 3 valores).

**Diego:** [5:48] Entonces, si viene un parámetro que no está dentro de los grupos de negocio actuales, ¿les pedimos que lo creen? **Gustavo:** [6:06] Sí: si tiene parámetros y no está en los definidos, avisen; si corresponde como grupo de negocio lo crean, si no, se va por URL.

**Diego:** [6:22] ¿Y si es por URL, cómo se agrega un parámetro? **Gustavo:** [6:28] Hasta ahora no hizo falta: los casos asignados son de póliza o de grupos ya agregados, así que no hay que preocuparse por ahora. **Diego:** [7:14] Hubo un ejemplo de póliza, pero los casos actuales no llevan parámetros.

**Martín:** [7:24] Ante cualquier duda sobre cómo van concatenados o qué parámetro pasar, consultarles.

### 3. Scripts pendientes y URL del ticket 4318 (7:35 – 8:43)

**Diego:** [7:35] Pasó en el chat todos los scripts que hay que ejecutar para avanzar con los tickets que faltan. [8:06] Están en el chat del grupo "Modernización de módulos" [?] (el ASR dice "Blog y moderniza sión de módulos"). **Martín:** [8:09] Los va a correr.

**Diego:** [8:16] Al final agregó que hay que agregar una **URL**; pueden consultarlo en la reunión con otra persona ("hijo" [?]). [8:28] Está en el **ticket 4318**, que llama a un form; no sabe si ese form ya está migrado. Menciona el form "artef 42 D 17" [?].

## Términos detectados

| Término | Variante en el audio | Qué significa según el video | Timestamp |
|---|---|---|---|
| Grupo de negocio | "grupo de negocio", "grupo de negociación", "grupo se negocia" | Configuración que convierte un campo en link a otra pantalla, con su propia clave | 0:18, 3:12 |
| Ver póliza / ver productor | igual | Nombre convencional del campo nuevo que actúa como link | 0:18 |
| Clave de póliza | "el ramo, la barra, el número de póliza, la barra, el certificado" | ramo/póliza/certificado concatenados | 0:18 |
| Clave de ingreso | "esquema, compañía, ingreso y el número de ingreso" | esquema + compañía de ingreso + número de ingreso | 6:56 |
| Parametría | "parametría" | Tablas de parametrización de la pantalla nueva | 0:05, 1:22 |
| Pasaje | "pasajes" | Pase del cambio entre ambientes | 3:48 |
| Póliza ART | "póliza ART" | Grupo de negocio para pólizas de ART | 3:12 |

## Reglas y casos especiales detectados

- [0:18] El grupo póliza recibe ramo/póliza/certificado concatenados con "/".
- [1:42] Para un link siempre se crea un campo nuevo; no se linkea sobre el campo de la tabla.
- [2:12] Productor: se pasa solo el número de productor (vía función, sin concatenar).
- [3:12] Grupos vigentes: póliza, ingreso, cuenta corriente, productor, cliente, procesos manuales, póliza ART.
- [3:48] Los grupos nuevos los agregan Gustavo/Martín; cada alta requiere hacer todos los pasajes.
- [6:06] Si el parámetro no encaja en un grupo existente: avisar; se decide entre grupo de negocio, link o URL.

## Pendientes / dudas abiertas

- [6:22] Cómo se agrega un parámetro cuando el link va por URL: no se respondió (no hizo falta hasta ahora).
- [4:42] Nombre/prefijo de la tabla de ingreso ("Pex t recaudo", "PXG/PXGRE", "Pexen") sin confirmar.
- [4:20] "Buffet": ¿documento o pantalla de referencia? Sin confirmar.
- [8:28] Ticket 4318: URL a agregar; verificar si el form "artef 42 D 17" [?] ya está migrado.
- [8:16] "hijo" [?]: persona a consultar por la URL.
