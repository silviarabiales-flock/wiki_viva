---
type: Término
title: Lista de valores (LOV)
description: Lista que se le muestra al usuario para elegir el valor de un campo; en el sistema nuevo se arma en el paquete con una plantilla, se engancha en "lista genérica" y se declara en la definición del campo (tipo A o S).
aliases: [LOV, lista de valores, "Love", "Lob", "logo", "Love esquema", "LOV ejemplo plantilla", "Love ejemplo plantilla", lista genérica, tipo de lista A/S]
dominio: tecnico
tags: [modernizacion-de-modulos, lov, lista-de-valores, lista-generica, plantilla, column-mapping, record-group, validador, descriptivos, edicion, alta]
estado: borrador
valida: referente técnico
fuentes: [charla-tecnica-modernizacion-modulos-4@1:33:31, charla-tecnica-modernizacion-modulos-4@1:28:00, charla-tecnica-modernizacion-modulos-4@1:28:26, charla-tecnica-modernizacion-modulos-4@1:29:43, charla-tecnica-modernizacion-modulos-4@1:30:14, charla-tecnica-modernizacion-modulos-6@16:45, charla-tecnica-modernizacion-modulos-4@3:14, charla-tecnica-modernizacion-modulos-4@3:42, charla-tecnica-modernizacion-modulos-4@6:02, charla-tecnica-modernizacion-modulos-4@6:29, charla-tecnica-modernizacion-modulos-4@6:53, charla-tecnica-modernizacion-modulos-4@1:30:44, charla-tecnica-modernizacion-modulos-4@1:31:13, charla-tecnica-modernizacion-modulos-4@1:31:40, charla-tecnica-modernizacion-modulos-4@1:32:06, charla-tecnica-modernizacion-modulos-4@1:32:31, charla-tecnica-modernizacion-modulos-4@1:33:00, charla-tecnica-modernizacion-modulos-4@1:35:51, charla-tecnica-modernizacion-modulos-4@1:34:32, charla-tecnica-modernizacion-modulos-4@1:35:21, charla-tecnica-modernizacion-modulos-4@1:46:52, charla-tecnica-modernizacion-modulos-4@1:39:15, charla-tecnica-modernizacion-modulos-4@1:39:41, charla-tecnica-modernizacion-modulos-4@1:40:04, charla-tecnica-modernizacion-modulos-4@1:42:25, charla-tecnica-modernizacion-modulos-4@1:43:17, charla-tecnica-modernizacion-modulos-4@1:43:46, charla-tecnica-modernizacion-modulos-4@1:36:20, charla-tecnica-modernizacion-modulos-4@1:37:17, charla-tecnica-modernizacion-modulos-4@1:37:41, charla-tecnica-modernizacion-modulos-4@1:45:04, charla-tecnica-modernizacion-modulos-6@25:44, charla-tecnica-modernizacion-modulos-6@28:01, charla-tecnica-modernizacion-modulos-6@16:16, charla-tecnica-modernizacion-modulos-6@29:27, charla-tecnica-modernizacion-modulos-6@30:21, charla-tecnica-modernizacion-modulos-6@30:52, charla-tecnica-modernizacion-modulos-6@28:31]
ultima_fuente: 2026-04-23
contradicciones: 0
---

# Lista de valores (LOV)

## Definición
La lista de valores (LOV) muestra al usuario una lista de códigos con su descripción para que elija uno, a diferencia del descriptivo, donde ya se tiene el código y solo hay que traer la descripción [Charla 4 · 1:33:31](../charla-tecnica-modernizacion-modulos-4.md). Cada lista de valores que tiene el Forms hay que armarla en el paquete, porque se usa en el alta o en la edición, y al modificar el campo tiene que aparecerle al usuario como en el Forms [Charla 4 · 1:28:00](../charla-tecnica-modernizacion-modulos-4.md) [Charla 4 · 1:28:26](../charla-tecnica-modernizacion-modulos-4.md).

En el paquete hay un procedimiento "lista genérica" que recibe el nombre del campo y con eso arma la lista; en el body está la plantilla "LOV ejemplo plantilla" [Charla 4 · 1:29:43](../charla-tecnica-modernizacion-modulos-4.md) [Charla 4 · 1:30:14](../charla-tecnica-modernizacion-modulos-4.md). La lista genérica funciona como "dame la lista de tal campo": pide de qué campo y devuelve la lista [Charla 6 · 16:45](../charla-tecnica-modernizacion-modulos-6.md).

## Detalle
- **En Forms, la LOV de un descriptivo está en el código:** en un ítem descriptivo la LOV no está en el propio ítem, sino en el campo anterior (el código) [Charla 4 · 3:14](../charla-tecnica-modernizacion-modulos-4.md). La LOV tiene un mapping código–descripción [Charla 4 · 3:42](../charla-tecnica-modernizacion-modulos-4.md) mediante la propiedad Column Mapping, y su query está en el Record Group [Charla 4 · 6:02](../charla-tecnica-modernizacion-modulos-4.md).
- **LOV y post-query:** cuando en Forms se hace una LOV con descripción, después hay que buscar el dato y llenarlo en el post-query; si no, la descripción queda vacía al consultar [Charla 4 · 6:29](../charla-tecnica-modernizacion-modulos-4.md). Aunque se haga la relación para traer el dato con un descriptivo, igual después hay que hacer la lista de valores [Charla 4 · 6:53](../charla-tecnica-modernizacion-modulos-4.md).
- **Armado con la plantilla:** copiar la plantilla completa, cambiar el nombre "LOV ejemplo" por el de la lista (también abajo) y cambiar el query [Charla 4 · 1:30:44](../charla-tecnica-modernizacion-modulos-4.md) [Charla 4 · 1:31:13](../charla-tecnica-modernizacion-modulos-4.md). El query se puede sacar del join ya hecho para el descriptivo [Charla 4 · 1:31:40](../charla-tecnica-modernizacion-modulos-4.md). La plantilla trae un ejemplo de moneda y la asignación al type, y arma lo necesario para el JSON [Charla 4 · 1:32:06](../charla-tecnica-modernizacion-modulos-4.md) [Charla 4 · 1:32:31](../charla-tecnica-modernizacion-modulos-4.md).
- **Query de la lista:** lleva código y descripción (con Ref Code, `RV_LOW_VALUE` como código y `RV_MEANING` como descripción) [Charla 4 · 1:32:31](../charla-tecnica-modernizacion-modulos-4.md); el orden no importa si se ponen los alias [Charla 4 · 1:33:00](../charla-tecnica-modernizacion-modulos-4.md). Con el query listo está el 90 % hecho [Charla 4 · 1:33:31](../charla-tecnica-modernizacion-modulos-4.md).
- **Display y destino:** se define qué ve el usuario en el combo (código, un guion y la descripción) [Charla 4 · 1:35:51](../charla-tecnica-modernizacion-modulos-4.md) y a qué campo va cada valor: el nombre del campo destino, no el alias [Charla 4 · 1:34:32](../charla-tecnica-modernizacion-modulos-4.md). Al seleccionar, el código va al campo código (lista pro) y la descripción a su descriptivo [Charla 4 · 1:35:21](../charla-tecnica-modernizacion-modulos-4.md).
- **Tres lugares a cargar:** armar el query, asignar lo que ve el usuario y asignar valor → campo (normalmente dos pares; hay casos con más) [Charla 4 · 1:46:52](../charla-tecnica-modernizacion-modulos-4.md).
- **Engancharla en lista genérica:** no alcanza con definir el procedimiento; en "lista genérica" hay un IF por nombre del campo y ahí se agrega la llamada al procedimiento de la lista [Charla 4 · 1:39:15](../charla-tecnica-modernizacion-modulos-4.md) [Charla 4 · 1:39:41](../charla-tecnica-modernizacion-modulos-4.md) [Charla 4 · 1:40:04](../charla-tecnica-modernizacion-modulos-4.md). El nombre es el del campo código (lista pro), no el del descriptivo [Charla 4 · 1:42:25](../charla-tecnica-modernizacion-modulos-4.md).
- **Declararla en la definición:** hay que indicar en la definición del campo, en la pantalla de parametrización, que tiene lista; si no, el Front no la pide [Charla 4 · 1:43:17](../charla-tecnica-modernizacion-modulos-4.md).
- **Tipo de lista A / S:** A (ayuda) permite poner un valor de la lista o cualquier otro; S solo permite valores de la lista [Charla 4 · 1:43:46](../charla-tecnica-modernizacion-modulos-4.md).
- **Visible en la edición:** la lista no aparece si en la edición no hay campos visibles [Charla 4 · 1:36:20](../charla-tecnica-modernizacion-modulos-4.md); el campo código se marca editable y la descripción no se edita, porque se completa sola [Charla 4 · 1:37:17](../charla-tecnica-modernizacion-modulos-4.md) [Charla 4 · 1:37:41](../charla-tecnica-modernizacion-modulos-4.md).
- **Listas distintas para alta y edición:** una lista puede ser solo para editar y otra distinta para dar de alta; se indica en la definición [Charla 4 · 1:45:04](../charla-tecnica-modernizacion-modulos-4.md).
- **LOV vs validador:** para que al cargar un código aparezca la descripción al costado hay dos maneras: una lista de valores donde el usuario elige, o el validate del campo, que carga la descripción [Charla 6 · 25:44](../charla-tecnica-modernizacion-modulos-6.md) [Charla 6 · 28:01](../charla-tecnica-modernizacion-modulos-6.md). Se puede traer una lista y además validar el campo cuando el usuario elige un dato [Charla 6 · 16:16](../charla-tecnica-modernizacion-modulos-6.md).
- **Preferencia:** el expositor prefiere la lista de valores cuando son pocos valores [Charla 6 · 29:27](../charla-tecnica-modernizacion-modulos-6.md); para aprender, se pidió implementar las dos alternativas para el Estado y habilitar una u otra para comparar [Charla 6 · 30:21](../charla-tecnica-modernizacion-modulos-6.md) [Charla 6 · 30:52](../charla-tecnica-modernizacion-modulos-6.md).
- **Valor fuera de la lista:** si el valor del Estado no está en su Record Group, se debería dar error; el Forms no lo hace y queda a preguntar [Charla 6 · 28:31](../charla-tecnica-modernizacion-modulos-6.md).

## Contradicciones
Sin contradicciones entre las fuentes. La Charla 4 describe la lista genérica como el procedimiento que recibe el nombre del campo y arma la lista [Charla 4 · 1:30:14](../charla-tecnica-modernizacion-modulos-4.md) y la Charla 6 la describe igual [Charla 6 · 16:45](../charla-tecnica-modernizacion-modulos-6.md); la Charla 6 agrega la comparación con el validador.

## Relacionados
- [Validador de campo](termino-validador-de-campo.md)
- [Descriptivo y POST-QUERY](termino-descriptivo-y-post-query.md)
- [Ref Code y Record Group](termino-ref-code-y-record-group.md)
- [Case Restriction](termino-case-restriction.md)

## Fuentes
| Video | Fecha | Minuto | Qué aporta |
|---|---|---|---|
| Charla 4 | 2026-04-02 | 3:14 – 6:53 | LOV en Forms: campo código, Column Mapping, Record Group, post-query |
| Charla 4 | 2026-04-02 | 1:28:00 – 1:46:52 | Armado en el paquete, plantilla, lista genérica, definición del campo, tipo A/S |
| Charla 6 | 2026-04-23 | 16:16, 16:45 | Lista genérica y relación con validar registro |
| Charla 6 | 2026-04-23 | 25:44 – 30:52 | LOV vs validador para el Estado; preferencia con pocos valores |
