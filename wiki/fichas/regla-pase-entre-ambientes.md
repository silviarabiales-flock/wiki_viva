---
type: Regla de negocio
title: Pase entre ambientes
description: Se carga en desa, se pasa a test y, desde test, se genera el script de la parametrización que se manda a prod junto con el paquete y el type.
aliases: [pase a prod, pase a producción, pasaje, pasajes, pases_gen, "actualizaciones gen", "general script migración", Endesa]
dominio: tecnico
tags: [pase-a-produccion, ambientes, desa, test, prod, parametrizacion, script, paquete, type]
estado: borrador
valida: referente técnico
fuentes: [charla-tecnica-modernizacion-modulos-4@52:13, charla-tecnica-modernizacion-modulos-4@1:10:02, charla-tecnica-modernizacion-modulos-4@1:49:10, charla-tecnica-modernizacion-modulos-4@1:49:38, charla-tecnica-modernizacion-modulos-4@1:50:05, charla-tecnica-modernizacion-modulos-4@1:50:34, charla-tecnica-modernizacion-modulos-4@1:51:02, charla-tecnica-modernizacion-modulos-4@1:51:28, charla-tecnica-modernizacion-modulos-4@1:51:57, charla-tecnica-modernizacion-modulos-4@1:52:28, charla-tecnica-modernizacion-modulos-4@1:52:56, charla-tecnica-modernizacion-modulos-4@1:53:24, charla-tecnica-modernizacion-modulos-6@3:28, capacitacion-validacion-compuesta-campo-fecha-2026-05-12@2:50, modernizacion-modulos-revision-avance-2026-06-16@3:48]
ultima_fuente: 2026-06-16
contradicciones: 0
---

# Pase entre ambientes

## Regla
El flujo de ambientes es: se carga en desa y se pasa a test; cuando está en test, se genera desde test el script por clave [Charla 4 · 1:51:02](../charla-tecnica-modernizacion-modulos-4.md). Para pasar a otro ambiente no alcanza con correr de nuevo el proceso genérico: hay que llevar el paquete y todos los datos cargados en las tablas de parametrización [Charla 4 · 1:49:10](../charla-tecnica-modernizacion-modulos-4.md).

Para el pase se generan 3 cosas: el script de la parametrización (se corre el proceso, se baja el script y se deja en "paquetes a pasar"), el paquete y el type; sin eso no se puede replicar [Charla 4 · 1:51:57](../charla-tecnica-modernizacion-modulos-4.md).

## Detalle
- **Script de pase de parametrización:** hay un paquete llamado `pases_gen` (nombre sin confirmar) [Charla 4 · 1:49:10](../charla-tecnica-modernizacion-modulos-4.md) con un procedimiento que arma el script con el insert de todos los datos de las tablas, en orden, y lo deja en un archivo TXT del sistema; se le pasa la clave [Charla 4 · 1:49:38](../charla-tecnica-modernizacion-modulos-4.md). La función está al final de la especificación del paquete [Charla 4 · 1:50:34](../charla-tecnica-modernizacion-modulos-4.md).
- Se ejecuta con la clave; el grupo no va porque se usa uno por defecto, y van el ID y la agrupación [Charla 4 · 1:51:02](../charla-tecnica-modernizacion-modulos-4.md).
- El script tiene los inserts de todas las tablas (son muchas) y se manda junto con el paquete [Charla 4 · 1:50:05](../charla-tecnica-modernizacion-modulos-4.md). El proceso genérico abarca el proceso, los campos, los permisos, las operatorias, las validaciones, etc.; antes se hacía a mano [Charla 4 · 1:51:28](../charla-tecnica-modernizacion-modulos-4.md).
- **Por qué desde test:** en test el usuario puede modificar cosas de nivel tabla que no afectan la programación (qué ve, qué no, cómo va) y dar el OK [Charla 4 · 1:52:28](../charla-tecnica-modernizacion-modulos-4.md). Por eso, para pasar a prod hay que regenerar desde test el script de inserts de las tablas de parametrización [Charla 4 · 1:53:24](../charla-tecnica-modernizacion-modulos-4.md).
- **Qué se manda a prod:** lo que está en test de las tablas de parametrización (qué se navega, qué se ve, si se generó un grupo nuevo, etc.), además del paquete y el type; el equipo tiene que hacer una tarea para el pase a producción [Charla 4 · 1:52:56](../charla-tecnica-modernizacion-modulos-4.md).
- **Cambios de base hechos en desa:** en la Charla 6 se agregó en desa ("Endesa", sin confirmar) la "prima" (posiblemente la PK, sin confirmar) y se confirmó que se guardó el script para pasarlo a test, porque sin él no funcionaba [Charla 6 · 3:28](../charla-tecnica-modernizacion-modulos-6.md).
- **Diferencias entre ambientes:** puede haber cosas en desa que todavía no están en test; por ejemplo, lo nuevo de los montos dejó de andar en test y hubo que hacer un ajuste [Charla 4 · 52:13](../charla-tecnica-modernizacion-modulos-4.md). En desa a veces no hay datos o los borran [Charla 4 · 1:10:02](../charla-tecnica-modernizacion-modulos-4.md).
- El desarrollo se trabaja en desa [Capacitación · 2:50](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- **Grupos de negocio:** cada vez que se agrega un grupo hay que hacer todos los pasajes para que funcione; por eso solo los agregan Gustavo/Martín [Revisión · 3:48](../modernizacion-modulos-revision-avance-2026-06-16.md).

## Contradicciones
Sin contradicciones entre las fuentes.

## Relacionados
- [Término: grupo de negocio](termino-grupo-de-negocio.md)
- [Regla: permisos sobre tablas relacionadas](regla-permisos-tablas-relacionadas.md)
- [Regla: títulos de todos los campos](regla-titulos-de-todos-los-campos.md)

## Fuentes
| Video | Fecha | Minuto | Qué aporta |
|---|---|---|---|
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 52:13 | Diferencia desa/test (montos en test) |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 1:10:02 | En desa a veces no hay datos |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 1:49:10 | No alcanza con correr el proceso; paquete `pases_gen` |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 1:49:38 | El procedimiento genera el TXT con los inserts |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 1:50:05 | Se manda junto con el paquete |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 1:50:34 | Ubicación de la función |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 1:51:02 | Parámetros y flujo desa → test |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 1:51:28 | Tablas que abarca el proceso |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 1:51:57 | Las 3 cosas del pase |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 1:52:28 | Por qué se genera desde test |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 1:52:56 | Qué se lleva a prod |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 1:53:24 | Regenerar desde test el script |
| [Charla 6](../charla-tecnica-modernizacion-modulos-6.md) | 2026-04-23 | 3:28 | Script de cambio de base guardado para pasar a test |
| [Capacitación](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md) | 2026-05-12 | 2:50 | Se trabaja en desa |
| [Revisión](../modernizacion-modulos-revision-avance-2026-06-16.md) | 2026-06-16 | 3:48 | Cada grupo nuevo requiere todos los pasajes |
