---
type: Regla de negocio
title: Link con campo nuevo
description: Para armar un link a otra pantalla se crea un campo nuevo asociado a un grupo de negocio; no se linkea sobre el campo de la tabla.
aliases: [ver póliza, ver productor, campo link, campo en azul]
dominio: ambos
tags: [grupo-de-negocio, links, parametria, definicion-de-campos]
estado: borrador
valida: ambos
fuentes: [charla-tecnica-modernizacion-modulos-4@16:39, charla-tecnica-modernizacion-modulos-4@17:08, charla-tecnica-modernizacion-modulos-4@17:55, charla-tecnica-modernizacion-modulos-4@18:24, modernizacion-modulos-revision-avance-2026-06-16@0:18, modernizacion-modulos-revision-avance-2026-06-16@1:22, modernizacion-modulos-revision-avance-2026-06-16@1:42, modernizacion-modulos-revision-avance-2026-06-16@2:12, modernizacion-modulos-revision-avance-2026-06-16@2:21, modernizacion-modulos-revision-avance-2026-06-16@4:08, modernizacion-modulos-revision-avance-2026-06-16@6:06]
ultima_fuente: 2026-06-16
contradicciones: 0
---

# Link con campo nuevo

## Regla
Aunque el valor sea único (por ejemplo, el productor), para el link se arma un campo nuevo; no se usa el campo de la tabla para linkear [Revisión · 1:42](../modernizacion-modulos-revision-avance-2026-06-16.md). Para trabajar un link con grupo de negocio hay que agregar un campo nuevo, que generalmente se llama "ver póliza" o "ver productor", aunque el nombre es solo una convención [Revisión · 0:18](../modernizacion-modulos-revision-avance-2026-06-16.md). Ya en la Charla 4 el grupo de negocio se presenta como lo que se usa cuando se crea un campo que va a ser un link a otra pantalla [Charla 4 · 17:08](../charla-tecnica-modernizacion-modulos-4.md).

## Detalle
- **Cuándo aplica:** siempre que se necesite un link a otra pantalla; los links habituales se arman siempre como grupo de negocio [Revisión · 1:42](../modernizacion-modulos-revision-avance-2026-06-16.md). Si el link es de póliza, ingreso o cualquiera de los grupos ya definidos, se crea un campo más y se siguen todos los pasos [Revisión · 4:08](../modernizacion-modulos-revision-avance-2026-06-16.md).
- **Qué lleva el campo nuevo:** el valor que espera el grupo. Para póliza, ramo + "/" + número de póliza + "/" + número de certificado, y en pantalla se muestra el campo "ver póliza" [Revisión · 0:18](../modernizacion-modulos-revision-avance-2026-06-16.md). Para productor, solo el número, obtenido con una función sin concatenar [Revisión · 2:12](../modernizacion-modulos-revision-avance-2026-06-16.md). Cada grupo tiene su propia configuración de clave [Charla 4 · 18:24](../charla-tecnica-modernizacion-modulos-4.md).
- **Configuración:** en el campo definido como grupo de negocio se indica el grupo que corresponde (por ejemplo, "póliza") [Revisión · 2:21](../modernizacion-modulos-revision-avance-2026-06-16.md). Al marcarlo en la parametría, el sistema busca el link solo [Revisión · 1:22](../modernizacion-modulos-revision-avance-2026-06-16.md).
- En un campo común de la definición, la columna de grupo de negocio va en null [Charla 4 · 16:39](../charla-tecnica-modernizacion-modulos-4.md).
- En pantalla el campo link aparece en azul y su contenido lo llena el programa [Charla 4 · 17:55](../charla-tecnica-modernizacion-modulos-4.md).
- **Excepción:** si el link tiene parámetros y no corresponde a ningún grupo definido, hay que avisar; si corresponde como grupo de negocio lo crean, si no, se va por URL [Revisión · 6:06](../modernizacion-modulos-revision-avance-2026-06-16.md).

## Contradicciones
Sin contradicciones entre las fuentes.

## Relacionados
- [Término: grupo de negocio](termino-grupo-de-negocio.md)
- [Término: descriptivo y post-query](termino-descriptivo-y-post-query.md)

## Fuentes
| Video | Fecha | Minuto | Qué aporta |
|---|---|---|---|
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 16:39 | Columna grupo de negocio en null para un campo común |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 17:08 | El grupo de negocio es para un campo que va a ser link |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 17:55 | El campo link se ve en azul y lo llena el programa |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 18:24 | Cada grupo tiene su clave |
| [Revisión](../modernizacion-modulos-revision-avance-2026-06-16.md) | 2026-06-16 | 0:18 | Agregar campo nuevo "ver póliza"/"ver productor" |
| [Revisión](../modernizacion-modulos-revision-avance-2026-06-16.md) | 2026-06-16 | 1:22 | La parametría busca el link sola |
| [Revisión](../modernizacion-modulos-revision-avance-2026-06-16.md) | 2026-06-16 | 1:42 | Regla: campo nuevo, no el de la tabla |
| [Revisión](../modernizacion-modulos-revision-avance-2026-06-16.md) | 2026-06-16 | 2:12 | Productor: valor por función |
| [Revisión](../modernizacion-modulos-revision-avance-2026-06-16.md) | 2026-06-16 | 2:21 | Indicar el grupo en el campo |
| [Revisión](../modernizacion-modulos-revision-avance-2026-06-16.md) | 2026-06-16 | 4:08 | Grupo existente: se crea un campo más |
| [Revisión](../modernizacion-modulos-revision-avance-2026-06-16.md) | 2026-06-16 | 6:06 | Sin grupo que encaje: avisar o URL |
