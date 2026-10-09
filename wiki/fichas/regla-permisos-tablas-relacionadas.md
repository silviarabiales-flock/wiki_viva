---
type: Regla de negocio
title: Permisos sobre la tabla migrada y sus relacionadas
description: Antes de generar hay que dar permisos a la tabla que se migra y a todas las tablas con las que se relaciona; los permisos de pantalla (consulta, edición, borrado) se ajustan aparte.
aliases: [grants, "gran", permisos de la tabla, permisos a las relacionadas]
dominio: tecnico
tags: [permisos, grants, migracion, relaciones, ref-code, sinonimo, parametrizacion]
estado: borrador
valida: referente técnico
fuentes: [charla-tecnica-modernizacion-modulos-4@0:30, charla-tecnica-modernizacion-modulos-4@0:58, charla-tecnica-modernizacion-modulos-4@1:21, charla-tecnica-modernizacion-modulos-4@1:50, charla-tecnica-modernizacion-modulos-4@14:02, charla-tecnica-modernizacion-modulos-4@14:25, charla-tecnica-modernizacion-modulos-4@14:54, charla-tecnica-modernizacion-modulos-4@40:12, charla-tecnica-modernizacion-modulos-4@1:21:24, charla-tecnica-modernizacion-modulos-4@1:24:22, charla-tecnica-modernizacion-modulos-4@1:26:04, charla-tecnica-modernizacion-modulos-4@1:26:34, charla-tecnica-modernizacion-modulos-4@1:27:01, charla-tecnica-modernizacion-modulos-4@1:28:26, charla-tecnica-modernizacion-modulos-4@1:45:56, charla-tecnica-modernizacion-modulos-4@1:51:28, charla-tecnica-modernizacion-modulos-6@34:02]
ultima_fuente: 2026-04-23
contradicciones: 0
---

# Permisos sobre la tabla migrada y sus relacionadas

## Regla
Hay que dar permiso tanto a la tabla que se va a migrar como a todas las tablas con las que se relaciona; si no, hay problemas en la generación, porque el script los necesita [Charla 4 · 1:21](../charla-tecnica-modernizacion-modulos-4.md). Es lo primero que se pregunta al arrancar: si se le pusieron permisos a la tabla que se está haciendo [Charla 4 · 0:30](../charla-tecnica-modernizacion-modulos-4.md). Por ejemplo, si la tabla tiene monedas y hay que relacionarla con la tabla de monedas, también hay que dar permisos a ese conjunto de tablas relacionadas [Charla 4 · 0:58](../charla-tecnica-modernizacion-modulos-4.md).

Los permisos hacen falta para que se pueda armar bien el script de relación, y hay que verificar todo ese proceso [Charla 4 · 1:50](../charla-tecnica-modernizacion-modulos-4.md).

## Detalle
- **Por qué:** con moneda, el proceso arma un script con la relación a la tabla de monedas y una condición del tipo "código de moneda igual a…" que después hay que completar [Charla 4 · 1:21](../charla-tecnica-modernizacion-modulos-4.md).
- **Tabla de Ref Codes:** hay que tener permisos sobre `CG_REF_CODES` (nombre sin confirmar) y verificarlo siempre, porque se está haciendo una relación [Charla 4 · 14:02](../charla-tecnica-modernizacion-modulos-4.md).
- **Sinónimos:** no hace falta anteponer el esquema, porque las tablas del esquema "valsec" (sin confirmar) tienen sinónimo para referenciarlas desde cualquier lado [Charla 4 · 14:25](../charla-tecnica-modernizacion-modulos-4.md). Pero un sinónimo no da acceso, solo referencia: igual hacen falta los permisos, y si no hay permiso no deja [Charla 4 · 14:54](../charla-tecnica-modernizacion-modulos-4.md).
- **Funciones reutilizadas:** la función de saldo de la póliza ya está resuelta, se llama desde unos 40 lugares y ya tiene los grants ("gran", sin confirmar); se la reutiliza en vez de reimplementarla [Charla 6 · 34:02](../charla-tecnica-modernizacion-modulos-6.md).
- **Permisos de pantalla (distintos de los de base):** se pueden ajustar después; para poder trabajar se pone 000 y luego se agregan los que se quieran [Charla 4 · 1:21:24](../charla-tecnica-modernizacion-modulos-4.md).
  - Sin permiso de borrado no aparece el botón borrar, y en esa tabla estaba bien así porque no se debe poder borrar [Charla 4 · 1:26:34](../charla-tecnica-modernizacion-modulos-4.md). El borrado podría habilitarse para algún permiso especial [Charla 4 · 1:45:56](../charla-tecnica-modernizacion-modulos-4.md).
  - En el ejemplo, insertar quedó con permiso 0 porque no se encontró cuál correspondía, y editar con permiso 33 (sin confirmar) [Charla 4 · 1:27:01](../charla-tecnica-modernizacion-modulos-4.md).
  - Con permisos el usuario puede consultar la tabla, pero no editarla hasta que se definan los campos editables, y eso lo tiene que dar el usuario [Charla 4 · 1:28:26](../charla-tecnica-modernizacion-modulos-4.md).
  - Se pueden tener vistas por nivel (resumida, nivel 1, nivel 2), cada una con su permiso [Charla 4 · 1:26:04](../charla-tecnica-modernizacion-modulos-4.md). Hay usuarios que, aunque tengan permiso, solo modifican 4 o 5 datos: puede convenir una vista restrictiva [Charla 4 · 1:24:22](../charla-tecnica-modernizacion-modulos-4.md).
- **Pantalla de parametrización:** cuando se migre la FDQM70000 (sin confirmar) habrá que separar usuario común de programador, que por permiso podrá modificar más [Charla 4 · 40:12](../charla-tecnica-modernizacion-modulos-4.md).
- **En el pase:** el proceso genérico abarca, entre otras tablas, las de permisos [Charla 4 · 1:51:28](../charla-tecnica-modernizacion-modulos-4.md).

## Contradicciones
Sin contradicciones entre las fuentes.

## Relacionados
- [Caso: una relación por tabla](caso-una-relacion-por-tabla.md)
- [Término: Ref Code y Record Group](termino-ref-code-y-record-group.md)
- [Regla: pase entre ambientes](regla-pase-entre-ambientes.md)

## Fuentes
| Video | Fecha | Minuto | Qué aporta |
|---|---|---|---|
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 0:30 | Pregunta inicial por los permisos de la tabla |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 0:58 | También a las tablas relacionadas (ej. monedas) |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 1:21 | Regla; el script de relación los necesita |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 1:50 | Verificar el proceso del script de relación |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 14:02 | Permisos sobre la tabla de Ref Codes |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 14:25 | Sinónimos para tablas de otros esquemas |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 14:54 | El sinónimo no da acceso |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 40:12 | Permiso de usuario común vs. programador en la FDQM70000 |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 1:21:24 | Permisos de pantalla: 000 y se ajustan después |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 1:24:22 | Vista restrictiva para usuarios con permiso |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 1:26:04 | Vistas por nivel con su permiso |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 1:26:34 | Sin permiso de borrado no aparece borrar |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 1:27:01 | Permisos de insert (0) y update (33, sin confirmar) |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 1:28:26 | Consultar sí, editar recién con campos editables |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 1:45:56 | Borrado solo para algún permiso especial |
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 1:51:28 | El pase incluye las tablas de permisos |
| [Charla 6](../charla-tecnica-modernizacion-modulos-6.md) | 2026-04-23 | 34:02 | La función de saldo ya tiene grants |
