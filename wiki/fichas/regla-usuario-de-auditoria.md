---
type: Regla de negocio
title: Usuario de auditoría
description: El usuario que hace la transacción se asigna en el backend antes del insert o update; no se pide, no se modifica ni se muestra en la pantalla.
aliases: [usuario, usuario de auditoría, usuario de la transacción, "va para usuario"]
dominio: ambos
tags: [usuario-auditoria, insert, update, validacion-pre-insert, definicion-del-insert, oracle-forms, migracion]
estado: borrador
valida: ambos
fuentes: [charla-tecnica-modernizacion-modulos-6@1:35, charla-tecnica-modernizacion-modulos-6@4:23, charla-tecnica-modernizacion-modulos-6@4:50, charla-tecnica-modernizacion-modulos-6@5:13, charla-tecnica-modernizacion-modulos-6@5:44, charla-tecnica-modernizacion-modulos-6@7:41, charla-tecnica-modernizacion-modulos-4@1:44:36, capacitacion-validacion-compuesta-campo-fecha-2026-05-12@19:58]
ultima_fuente: 2026-05-12
contradicciones: 0
---

# Usuario de auditoría

## Regla
Hay que guardar el usuario que hace la transacción, es decir, el que modifica o inserta el dato, y no el que queda figurando en la tabla [Charla 6 · 1:35](../charla-tecnica-modernizacion-modulos-6.md). En el Forms el usuario se manipula "por atrás": no importa lo que se ponga en el campo usuario, se pone el usuario que hizo la transacción [Charla 6 · 4:50](../charla-tecnica-modernizacion-modulos-6.md). Antes de insertar se pone el usuario real, sin importar lo tipeado, así que la pantalla nueva no puede dejar meter cualquier cosa ahí [Charla 6 · 5:13](../charla-tecnica-modernizacion-modulos-6.md).

En la definición del insert hay que establecer que el usuario no se puede modificar, o directamente no mostrarlo: en esa definición el usuario no debería usarse [Charla 6 · 4:23](../charla-tecnica-modernizacion-modulos-6.md). La asignación se hace en el backend, en el procedimiento que corre antes de insertar o antes del insert propiamente dicho, pero siempre antes de insertar en la tabla: si se pone después, no inserta nada [Charla 6 · 5:44](../charla-tecnica-modernizacion-modulos-6.md).

## Detalle
- **Problema detectado:** en la pantalla nueva no se estaba insertando el usuario [Charla 6 · 1:09](../charla-tecnica-modernizacion-modulos-6.md); en la prueba el campo usuario aparecía vacío [Charla 6 · 2:28](../charla-tecnica-modernizacion-modulos-6.md) y se confirmó que no se cargaba [Charla 6 · 3:28](../charla-tecnica-modernizacion-modulos-6.md). Además el campo era modificable y se podía escribir cualquier cosa, cuando lo que se necesita es quién realmente hizo el insert [Charla 6 · 3:54](../charla-tecnica-modernizacion-modulos-6.md).
- En el Forms el usuario se pone automáticamente al insertar; en el sistema nuevo por ahora no hay manera de ponerlo automático, aunque se podría [Charla 6 · 2:02](../charla-tecnica-modernizacion-modulos-6.md).
- **Dónde asignarlo:** se puede poner arriba, antes de hacer el insert, o en el procedimiento de validación pre-insert, cuyo nombre exacto no se recordó [Charla 6 · 6:13](../charla-tecnica-modernizacion-modulos-6.md). Ese procedimiento es un validador: antes de insertar llena campos, controla y da error si falta algo; a veces conviene asignar justo antes del insert por performance o para no dejar bloqueado mucho tiempo un registro [Charla 6 · 6:43](../charla-tecnica-modernizacion-modulos-6.md).
- **Criterio general:** todo lo que no afecte ni bloquee y haya que validar o completar va en el validador; cuando termina, se asignan los valores y se llama al insert, que inserta en esa tabla o en otras [Charla 6 · 7:11](../charla-tecnica-modernizacion-modulos-6.md).
- **Mismo criterio que el update:** el usuario se puede asignar en cualquiera de los dos procedimientos, pero lo mejor es hacerlo en pre-insert, así como en el update se hace en el "pre" (nombre sin confirmar), para que quede uniforme [Charla 6 · 7:41](../charla-tecnica-modernizacion-modulos-6.md). En la revisión del update ya resuelto, el Forms hacía lo mismo con el usuario que el código [Charla 6 · 0:40](../charla-tecnica-modernizacion-modulos-6.md).
- Ahí va todo lo simple que hace referencia al mismo registro; en la versión revisada el campo se seteaba después del insert, por lo que nunca se iba a insertar [Charla 6 · 8:02](../charla-tecnica-modernizacion-modulos-6.md).
- En la Charla 4 ya se había mencionado que antes del update hay un pre-update donde se pueden verificar cosas o llenar datos, y que todo eso se maneja desde atrás [Charla 4 · 1:44:36](../charla-tecnica-modernizacion-modulos-4.md).
- Los validadores del paquete reciben el usuario por parámetro, por si hace falta [Capacitación · 19:58](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).

## Contradicciones
Sin contradicciones entre las fuentes.

## Relacionados
- [Validador de campo](termino-validador-de-campo.md)
- [Títulos de todos los campos](regla-titulos-de-todos-los-campos.md)

## Fuentes
| Video | Fecha | Minuto | Qué aporta |
|---|---|---|---|
| [Charla 4](../charla-tecnica-modernizacion-modulos-4.md) | 2026-04-02 | 1:44:36 | El pre-update verifica y llena datos desde atrás |
| [Charla 6](../charla-tecnica-modernizacion-modulos-6.md) | 2026-04-23 | 0:40, 1:09, 1:35, 2:02, 2:28, 3:28, 3:54 | Qué usuario se guarda y problema detectado en la pantalla nueva |
| [Charla 6](../charla-tecnica-modernizacion-modulos-6.md) | 2026-04-23 | 4:23, 4:50, 5:13 | No se modifica ni se muestra; en Forms se asigna por atrás |
| [Charla 6](../charla-tecnica-modernizacion-modulos-6.md) | 2026-04-23 | 5:44, 6:13, 6:43, 7:11, 7:41, 8:02 | Asignación antes del insert (pre-insert), igual que en el update |
| [Capacitación](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md) | 2026-05-12 | 19:58 | Los validadores reciben el usuario por parámetro |
