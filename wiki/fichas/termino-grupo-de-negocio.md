---
type: Término
title: Grupo de negocio
description: Configuración que convierte un campo en un link a otra pantalla (póliza, productor, ingreso, etc.), con su propia clave.
aliases: [grupo negocio, grupo negocio póliza, grupo de negociación, grupo se negocia]
dominio: ambos
tags: [grupo-de-negocio, links, parametria, poliza, productor, ingreso, siniestro]
estado: borrador
valida: ambos
fuentes: [charla-tecnica-modernizacion-modulos-4@16:39, charla-tecnica-modernizacion-modulos-4@17:08, charla-tecnica-modernizacion-modulos-4@17:28, charla-tecnica-modernizacion-modulos-4@17:55, charla-tecnica-modernizacion-modulos-4@18:24, charla-tecnica-modernizacion-modulos-4@18:54, charla-tecnica-modernizacion-modulos-4@19:20, modernizacion-modulos-revision-avance-2026-06-16@0:18, modernizacion-modulos-revision-avance-2026-06-16@1:22, modernizacion-modulos-revision-avance-2026-06-16@1:42, modernizacion-modulos-revision-avance-2026-06-16@2:12, modernizacion-modulos-revision-avance-2026-06-16@2:21, modernizacion-modulos-revision-avance-2026-06-16@3:04, modernizacion-modulos-revision-avance-2026-06-16@3:12, modernizacion-modulos-revision-avance-2026-06-16@3:48, modernizacion-modulos-revision-avance-2026-06-16@4:08, modernizacion-modulos-revision-avance-2026-06-16@4:26, modernizacion-modulos-revision-avance-2026-06-16@6:06, modernizacion-modulos-revision-avance-2026-06-16@6:28, modernizacion-modulos-revision-avance-2026-06-16@6:56, modernizacion-modulos-revision-avance-2026-06-16@7:24]
ultima_fuente: 2026-06-16
contradicciones: 0
---

# Grupo de negocio

## Definición
Un grupo de negocio se usa cuando se crea un campo que va a ser un link para ir a otra pantalla [Charla 4 · 17:08](../charla-tecnica-modernizacion-modulos-4.md). Por ejemplo, desde una tabla con la póliza se puede ir, con un clic, a la consulta de póliza, que tiene una URL determinada [Charla 4 · 17:28](../charla-tecnica-modernizacion-modulos-4.md). Es la forma estándar de armar los links habituales [Revisión · 1:42](../modernizacion-modulos-revision-avance-2026-06-16.md).

En pantalla el campo aparece en azul y su contenido lo llena el programa [Charla 4 · 17:55](../charla-tecnica-modernizacion-modulos-4.md). Cada grupo tiene su propia configuración de clave, que es el valor con el que se va a buscar en la pantalla destino [Charla 4 · 18:24](../charla-tecnica-modernizacion-modulos-4.md). Cuando el usuario hace clic, se llama a un servicio propio que le indica a dónde tiene que ir y lo lleva solo, lo que permite ir integrando el sistema con otros [Charla 4 · 18:54](../charla-tecnica-modernizacion-modulos-4.md). Al indicar en la parametría que el campo corresponde a un grupo de negocio, el sistema busca el link solo, porque todo está en tabla [Revisión · 1:22](../modernizacion-modulos-revision-avance-2026-06-16.md).

## Detalle
- **Cómo se usa:** se agrega un campo nuevo, que por convención se llama "ver póliza" o "ver productor" [Revisión · 0:18](../modernizacion-modulos-revision-avance-2026-06-16.md). Si el link es de un grupo ya definido, se crea un campo más y se siguen todos los pasos [Revisión · 4:08](../modernizacion-modulos-revision-avance-2026-06-16.md). En el campo definido como grupo de negocio se pone el grupo que corresponde (por ejemplo, "póliza") [Revisión · 2:21](../modernizacion-modulos-revision-avance-2026-06-16.md).
- En la definición de campos hay una columna para el grupo de negocio, que en un campo común (por ejemplo, el de la Red Code) va en null [Charla 4 · 16:39](../charla-tecnica-modernizacion-modulos-4.md).
- **Clave del grupo póliza:** ramo + "/" + número de póliza + "/" + número de certificado [Revisión · 0:18](../modernizacion-modulos-revision-avance-2026-06-16.md); en la Charla 4 se ve como algo del tipo "4/número/0" (ramo/póliza/certificado) [Charla 4 · 18:24](../charla-tecnica-modernizacion-modulos-4.md).
- **Clave del grupo productor:** solo el número de productor [Revisión · 1:42](../modernizacion-modulos-revision-avance-2026-06-16.md), que se obtiene con una función, sin concatenar nada [Revisión · 2:12](../modernizacion-modulos-revision-avance-2026-06-16.md).
- **Clave del grupo ingreso:** concatenación de esquema, compañía de ingreso y número de ingreso [Revisión · 6:56](../modernizacion-modulos-revision-avance-2026-06-16.md).
- **Clave del grupo siniestro:** otros valores (serie, ramo, siniestro) [Charla 4 · 18:24](../charla-tecnica-modernizacion-modulos-4.md). En la Charla 4 el grupo siniestro se menciona como previsto ("va a haber un grupo siniestro") [Charla 4 · 17:28](../charla-tecnica-modernizacion-modulos-4.md); no figura en la lista de grupos definidos de la Revisión [Revisión · 3:12](../modernizacion-modulos-revision-avance-2026-06-16.md).
- **Grupos vigentes (al 16/06/2026):** póliza, ingreso, cuenta corriente, productor, cliente, procesos manuales y póliza ART [Revisión · 3:12](../modernizacion-modulos-revision-avance-2026-06-16.md). El grupo póliza ya existía y estaba probado en la Charla 4 [Charla 4 · 17:08](../charla-tecnica-modernizacion-modulos-4.md).
- **Dónde se definen:** en una función (no en un procedimiento), la última del listado [Revisión · 3:04](../modernizacion-modulos-revision-avance-2026-06-16.md).
- **Cómo pedir uno nuevo:** si un link con parámetros no corresponde a ninguno de los grupos existentes, hay que avisarles a Gustavo/Martín y ellos lo agregan; no se modifica la función por cuenta propia, porque cada alta requiere hacer todos los pasajes y ellos evalúan si corresponde grupo de negocio, link o URL [Revisión · 3:48](../modernizacion-modulos-revision-avance-2026-06-16.md). Si corresponde como grupo de negocio lo crean; si no, se va por URL [Revisión · 6:06](../modernizacion-modulos-revision-avance-2026-06-16.md).
- Cómo agregar un parámetro cuando el link va por URL todavía no hizo falta, porque los casos asignados son de póliza o de grupos ya agregados [Revisión · 6:28](../modernizacion-modulos-revision-avance-2026-06-16.md).
- **Modelo a seguir:** el ejemplo existente que tiene póliza y productor [Revisión · 4:26](../modernizacion-modulos-revision-avance-2026-06-16.md). Ante dudas sobre cómo van concatenados los valores o qué parámetro pasar, consultarles [Revisión · 7:24](../modernizacion-modulos-revision-avance-2026-06-16.md).
- Según la Charla 4, el link a consulta de póliza ya funcionaba en "Orion" (sin confirmar) [Charla 4 · 19:20](../charla-tecnica-modernizacion-modulos-4.md).

## Contradicciones
Sin contradicciones entre las fuentes.

## Relacionados
- [Regla: link con campo nuevo](regla-link-con-campo-nuevo.md)
- [Regla: pase entre ambientes](regla-pase-entre-ambientes.md)
- [Término: valor compuesto](termino-valor-compuesto.md)

## Fuentes
| Video | Fecha | Minuto | Qué aporta |
|---|---|---|---|
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 16:39 | Columna de grupo de negocio en la definición (null en un campo común) |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 17:08 | Para qué sirve; el grupo póliza ya existe y funciona |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 17:28 | Ejemplo de consulta de póliza; grupo siniestro previsto |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 17:55 | Grupo productor; campo en azul que llena el programa |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 18:24 | Clave por grupo: póliza "4/número/0", siniestro serie/ramo/siniestro |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 18:54 | Al hacer clic, un servicio propio indica a dónde ir |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 19:20 | Ya funciona en "Orion" (sin confirmar) |
| [Revisión](../modernizacion-modulos-revision-avance-2026-06-16.md) | 2026-06-16 | 0:18 | Campo nuevo "ver póliza"; clave ramo/póliza/certificado |
| [Revisión](../modernizacion-modulos-revision-avance-2026-06-16.md) | 2026-06-16 | 1:22 | La parametría resuelve el link sola (todo en tabla) |
| [Revisión](../modernizacion-modulos-revision-avance-2026-06-16.md) | 2026-06-16 | 1:42 | Los links habituales siempre son grupo de negocio; productor |
| [Revisión](../modernizacion-modulos-revision-avance-2026-06-16.md) | 2026-06-16 | 2:12 | Productor: valor por función, sin concatenar |
| [Revisión](../modernizacion-modulos-revision-avance-2026-06-16.md) | 2026-06-16 | 2:21 | En el campo se indica el grupo ("póliza") |
| [Revisión](../modernizacion-modulos-revision-avance-2026-06-16.md) | 2026-06-16 | 3:04 | Los grupos se definen en una función |
| [Revisión](../modernizacion-modulos-revision-avance-2026-06-16.md) | 2026-06-16 | 3:12 | Lista de grupos vigentes |
| [Revisión](../modernizacion-modulos-revision-avance-2026-06-16.md) | 2026-06-16 | 3:48 | Grupos nuevos: avisar; requieren pasajes |
| [Revisión](../modernizacion-modulos-revision-avance-2026-06-16.md) | 2026-06-16 | 4:08 | Grupo existente: se crea un campo más |
| [Revisión](../modernizacion-modulos-revision-avance-2026-06-16.md) | 2026-06-16 | 4:26 | Ejemplo modelo con póliza y productor |
| [Revisión](../modernizacion-modulos-revision-avance-2026-06-16.md) | 2026-06-16 | 6:06 | Si no corresponde a un grupo, se va por URL |
| [Revisión](../modernizacion-modulos-revision-avance-2026-06-16.md) | 2026-06-16 | 6:28 | Parámetros por URL: todavía no hizo falta |
| [Revisión](../modernizacion-modulos-revision-avance-2026-06-16.md) | 2026-06-16 | 6:56 | Clave del grupo ingreso |
| [Revisión](../modernizacion-modulos-revision-avance-2026-06-16.md) | 2026-06-16 | 7:24 | Consultar dudas de concatenación |
