---
type: Término
title: Ref Code y Record Group
description: Ref Code es la tabla de códigos/dominios para campos con valores fijos (CG_REF_CODES, sin confirmar); Record Group es el query de Forms que alimenta una LOV. Se usan de forma distinta en la migración.
aliases: [Ref Code, Ref Codes, "Red Code", "red Cow", "rescover", "res code", "refcode", "CG Red Code", "CG rescover", CG_REF_CODES (sin confirmar), Record Group, "record Group", RG, "recor Grupo", "rector" (a veces), "red Code" (en la Charla 6, leído como Record Group)]
dominio: tecnico
tags: [modernizacion-de-modulos, ref-code, record-group, cg-ref-codes, dominio, rv-meaning, rv-low-value, lov, oracle-forms, definicion-de-campos, join, permisos]
estado: borrador
valida: referente técnico
fuentes: [charla-tecnica-modernizacion-modulos-4@10:14, charla-tecnica-modernizacion-modulos-4@13:31, charla-tecnica-modernizacion-modulos-4@54:49, charla-tecnica-modernizacion-modulos-4@55:32, charla-tecnica-modernizacion-modulos-4@6:02, charla-tecnica-modernizacion-modulos-4@7:52, charla-tecnica-modernizacion-modulos-4@8:22, charla-tecnica-modernizacion-modulos-4@14:02, charla-tecnica-modernizacion-modulos-4@8:50, charla-tecnica-modernizacion-modulos-4@9:19, charla-tecnica-modernizacion-modulos-4@15:27, charla-tecnica-modernizacion-modulos-4@16:10, charla-tecnica-modernizacion-modulos-4@53:50, charla-tecnica-modernizacion-modulos-4@54:19, charla-tecnica-modernizacion-modulos-4@1:00:22, charla-tecnica-modernizacion-modulos-4@1:10:02, charla-tecnica-modernizacion-modulos-4@1:32:31, charla-tecnica-modernizacion-modulos-4@7:23, charla-tecnica-modernizacion-modulos-4@1:06:19, charla-tecnica-modernizacion-modulos-4@1:06:46, charla-tecnica-modernizacion-modulos-6@28:31, charla-tecnica-modernizacion-modulos-4@4:41, charla-tecnica-modernizacion-modulos-4@30:01, capacitacion-validacion-compuesta-campo-fecha-2026-05-12@40:48]
ultima_fuente: 2026-05-12
contradicciones: 2
---

# Ref Code y Record Group

## Definición
La **Ref Code** es la tabla donde van los valores fijos de un campo: si un campo tiene distintos valores fijos, siempre va a la Ref Code para no generar una tabla con esos valores [Charla 4 · 10:14](../charla-tecnica-modernizacion-modulos-4.md). El nombre de la tabla que se carga en la definición es "CG Red Code", es decir `CG_REF_CODES` (nombre sin confirmar) [Charla 4 · 13:31](../charla-tecnica-modernizacion-modulos-4.md). La relación con la Ref Code se arma con dos condiciones, el dominio y el código (low value, `RV_LOW_VALUE`, sin confirmar), igual que el WHERE que tiene el Forms [Charla 4 · 54:49](../charla-tecnica-modernizacion-modulos-4.md) [Charla 4 · 55:32](../charla-tecnica-modernizacion-modulos-4.md).

El **Record Group** es un objeto de Forms: es el select de la LOV que hay que copiarse para llevarlo al query [Charla 4 · 6:02](../charla-tecnica-modernizacion-modulos-4.md). Cada LOV tiene su Record Group y los Record Groups son distintos queries [Charla 4 · 7:52](../charla-tecnica-modernizacion-modulos-4.md). Mientras la Ref Code es una tabla que se referencia desde la definición del sistema nuevo, el Record Group es de dónde se saca el query (código y descripción) para copiarlo tal cual [Charla 4 · 8:22](../charla-tecnica-modernizacion-modulos-4.md).

## Detalle
- **Ref Code en la definición:** en la última columna del campo va el nombre de la tabla de Ref Code, entre comillas simples y en mayúsculas; conviene copiarlo de otro registro que se sepa que funciona [Charla 4 · 13:31](../charla-tecnica-modernizacion-modulos-4.md) [Charla 4 · 14:02](../charla-tecnica-modernizacion-modulos-4.md).
- **Una sola vez por definición:** la Ref Code puede ir una sola vez en la definición; se elige un campo, a ese se le pone la tabla Ref Code y al resto null [Charla 4 · 8:50](../charla-tecnica-modernizacion-modulos-4.md) [Charla 4 · 9:19](../charla-tecnica-modernizacion-modulos-4.md). Ver [Una sola relación por tabla](caso-una-relacion-por-tabla.md).
- **Campo de la descripción:** el nombre del campo se saca del query de la Ref Code [Charla 4 · 15:27](../charla-tecnica-modernizacion-modulos-4.md); es `RV_MEANING` (sin confirmar), el campo que se llena con la Ref Code [Charla 4 · 16:10](../charla-tecnica-modernizacion-modulos-4.md).
- **Caso especial:** el campo de la Ref Code es casi siempre `RV_MEANING`; hay casos muy especiales en que puede ser otro (el 99 % es ese), así que igual hay que verificarlo [Charla 4 · 16:10](../charla-tecnica-modernizacion-modulos-4.md).
- **Nombre de las Ref Codes:** normalmente llevan el nombre de la tabla y además deberían llevar el nombre del campo al que hacen referencia (por ejemplo, las que van a cajero o a productor) [Charla 4 · 8:50](../charla-tecnica-modernizacion-modulos-4.md).
- **Permisos:** hay que tener permisos sobre `CG_REF_CODES` y verificarlo siempre, porque se está haciendo una relación [Charla 4 · 14:02](../charla-tecnica-modernizacion-modulos-4.md).
- **Join en el paquete:** el dominio está escrito en el query de origen (cuidado con la doble comilla) [Charla 4 · 53:50](../charla-tecnica-modernizacion-modulos-4.md) y el código aparece con dos puntos; se pone el nombre del campo sin los dos puntos [Charla 4 · 54:19](../charla-tecnica-modernizacion-modulos-4.md) [Charla 4 · 54:49](../charla-tecnica-modernizacion-modulos-4.md). Como dominio más código no es clave primaria, el bloque debería manejar NO_DATA_FOUND y TOO_MANY_ROWS [Charla 4 · 1:00:22](../charla-tecnica-modernizacion-modulos-4.md).
- **Pruebas:** si un descriptivo no trae datos, se ejecuta la consulta en la Ref Code en desa; a veces en desa no hay datos o los borran [Charla 4 · 1:10:02](../charla-tecnica-modernizacion-modulos-4.md).
- **Lista de valores con Ref Code:** el select de la LOV toma `RV_MEANING` como descripción y `RV_LOW_VALUE` como código [Charla 4 · 1:32:31](../charla-tecnica-modernizacion-modulos-4.md).
- **Record Group en la práctica:** para un descriptivo que no se llena, buscar la LOV, ver cuál es su Record Group y entrar ahí [Charla 4 · 7:52](../charla-tecnica-modernizacion-modulos-4.md). El Record Group arma un select con código y descripción, y el Column Mapping de la LOV indica a qué campo va cada uno [Charla 4 · 7:23](../charla-tecnica-modernizacion-modulos-4.md).
- **Copiar del Record Group al paquete:** como el Record Group no tiene el BEGIN/EXCEPTION, se toma un bloque ya pegado y se le cambia el query (en el ejemplo, el dominio de esquema) [Charla 4 · 1:06:19](../charla-tecnica-modernizacion-modulos-4.md) [Charla 4 · 1:06:46](../charla-tecnica-modernizacion-modulos-4.md).
- **Record Group como fuente de valores válidos:** para el campo Estado, si el valor no está en el Record Group se debería dar error (en Forms no lo hace; queda a preguntar) [Charla 6 · 28:31](../charla-tecnica-modernizacion-modulos-6.md).

## Contradicciones
> ⚠ **Contradicción (de interpretación del audio):** en la [Charla 4 · 4:41](../charla-tecnica-modernizacion-modulos-4.md) "Red Code" se interpreta como Ref Code (tabla `CG_REF_CODES`, ver también [Charla 4 · 13:31](../charla-tecnica-modernizacion-modulos-4.md)); en la [Charla 6 · 28:31](../charla-tecnica-modernizacion-modulos-6.md) el mismo sonido "red Code" se interpreta como Record Group (origen de los valores válidos del Estado). **Vigente: Charla 6** para ese contexto (ante contradicción prevalece la Charla 6). Aclaración honesta: no es un desacuerdo sobre cómo funciona el negocio, sino sobre qué palabra hay detrás del audio; cada lectura se apoya en su propio contexto y la de la Charla 4 se mantiene para los pasajes sobre `CG_REF_CODES`, dominio y `RV_MEANING`. Por eso "red Code" no debe leerse automáticamente como Ref Code.

> ⚠ **Contradicción (de interpretación del audio):** en la [Charla 4 · 30:01](../charla-tecnica-modernizacion-modulos-4.md) "rector" se interpreta (sin confirmar) como la pantalla de parametrización; en la [Capacitación · 40:48](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md) "rector" se interpreta como Record Group (lugar desde donde también se modificaría el indicador de campo query). **Vigente: Capacitación** (fuente más reciente), **a confirmar**. Igual que la anterior, es una divergencia de lectura del audio, no de contenido.

## Relacionados
- [Lista de valores](termino-lista-de-valores.md)
- [Descriptivo y POST-QUERY](termino-descriptivo-y-post-query.md)
- [Una sola relación por tabla](caso-una-relacion-por-tabla.md)
- [Permisos sobre tablas relacionadas](regla-permisos-tablas-relacionadas.md)
- [Validador de campo](termino-validador-de-campo.md)
- [Campo query](termino-campo-query.md)

## Fuentes
| Video | Fecha | Minuto | Qué aporta |
|---|---|---|---|
| Charla 4 | 2026-04-02 | 6:02 – 8:22 | Record Group como query de la LOV; Column Mapping; copiar el query |
| Charla 4 | 2026-04-02 | 8:50 – 16:10 | Ref Code: valores fijos, nombre de la tabla, una vez por definición, `RV_MEANING`, permisos |
| Charla 4 | 2026-04-02 | 53:50 – 1:06:46 | Join con la Ref Code por dominio y low value; bloque copiado del Record Group |
| Charla 6 | 2026-04-23 | 28:31 | "red Code" leído como Record Group de los valores válidos del Estado |
| Capacitación | 2026-05-12 | 40:48 | "rector" leído como Record Group |
