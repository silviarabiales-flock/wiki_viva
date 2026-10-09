---
type: Término
title: Valor compuesto
description: Campo de filtro (fecha o numérico) que recibe dos valores, desde y hasta, en lugar de uno; el Front arma el filtro y el back solo usa los dos valores para validar.
aliases: [validación compuesta, valida compuesto, campo compuesto, fecha compuesta, "combinado", "numéricos combinados", fecha desde / fecha hasta]
dominio: tecnico
tags: [valor-compuesto, campo-fecha, operatoria, filtro, json, type, rectype, campos-auxiliares, validador, parametrizacion]
estado: borrador
valida: referente técnico
fuentes: [capacitacion-validacion-compuesta-campo-fecha-2026-05-12@1:25, capacitacion-validacion-compuesta-campo-fecha-2026-05-12@7:43, capacitacion-validacion-compuesta-campo-fecha-2026-05-12@9:13, capacitacion-validacion-compuesta-campo-fecha-2026-05-12@12:38, capacitacion-validacion-compuesta-campo-fecha-2026-05-12@15:23, capacitacion-validacion-compuesta-campo-fecha-2026-05-12@28:30]
ultima_fuente: 2026-05-12
contradicciones: 0
---

# Valor compuesto

## Definición
Un valor compuesto es un campo, numérico o de fecha, para el que el Front no manda un solo valor sino dos, con un formato especial que el Front genera automáticamente [Capacitación · 1:25](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). Normalmente el Front manda un JSON con el nombre de cada campo y su dato, y un transformador lo convierte al type, que usa los mismos nombres de campo [Capacitación · 0:56](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).

Se usa cuando la operatoria del Forms tiene fecha desde y fecha hasta sobre un mismo campo: al definir la operatoria se indica que ese campo es compuesto, aunque en la tabla haya una sola fecha [Capacitación · 7:43](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). Con el campo marcado como compuesto, el Front muestra dos fechas y pasa los datos al back para validarlos, pero el "fecha entre desde y hasta" lo arma el Front [Capacitación · 9:13](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).

## Detalle
- **Quién arma el filtro:** el back no filtra ni arma ningún WHERE con las dos fechas; eso lo hace el Front [Capacitación · 9:41](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- El WHERE del bloque del Forms se pasa al filtro de la operatoria, salvo la parte de las fechas, que llega por parámetro [Capacitación · 6:51](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). En la operatoria va ese WHERE sin la parte de la fecha [Capacitación · 29:29](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- **Opciones de validación del filtro** (en la operatoria, en el filtro) [Capacitación · 28:30](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md):
  - *Valida*: el Front muestra una sola fecha y se valida sobre ese único campo, sin campos adicionales.
  - *Valida compuesto*: el Front muestra dos fechas y hay que programar en el type dónde guardar la segunda y validarlas.
  - *No valida*: el Front muestra dos fechas y no hay que programar nada ni tocar el type.
- En la parametrización, el campo fecha del caso trabajado lleva un validador compuesto [Capacitación · 28:00](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- **Campos auxiliares:** el caso arranca generando campos auxiliares de consulta [Capacitación · 0:02](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md), donde se guardan fecha desde y fecha hasta para validarlas, del lado del type [Capacitación · 0:29](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). No conviene agregar "fecha desde/fecha hasta" como campos comunes de la definición [Capacitación · 8:13](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). Solo hacen falta si hay que validar el rango [Capacitación · 9:41](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md); pueden quedar en nulo [Capacitación · 10:42](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). Con los numéricos compuestos se hace exactamente lo mismo [Capacitación · 11:09](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- **"Obtener valores del JSON fecha":** el procedimiento del type que construye el registro desde el JSON asigna cada dato a un solo campo, y para la fecha compuesta llegan dos valores [Capacitación · 12:13](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). Para eso hay plantillas de dos procedimientos; para fechas se usa "obtener valores del JSON fecha" [Capacitación · 12:38](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). Se llama solo si llega el campo y se lo definió como compuesto en la parametría [Capacitación · 13:11](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). Recibe el JSON, el formato de fecha (que puede incluir hora) y el valor del campo [Capacitación · 13:44](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). Devuelve el mismo valor único si el campo no es compuesto, o fecha desde y fecha hasta si lo es [Capacitación · 14:26](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). En el ejemplo, la primera fecha va al campo fecha y desde/hasta a los auxiliares [Capacitación · 14:57](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- **Rendimiento:** no se llama al procedimiento en todos los campos fecha, porque en el ~95 % de los casos no son compuestos y cada fecha necesitaría su par desde/hasta (5 fechas serían 15 campos) [Capacitación · 15:23](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- Los campos desde/hasta se cargan con el único objetivo de validar, y con los numéricos compuestos ("combinados") se procede igual [Capacitación · 17:03](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). Lo que sigue va en el procedimiento de validación [Capacitación · 17:58](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- **Validación:** en el paquete, el procedimiento "validar operatoria de filtro" ya tiene cargados el campo fecha y los auxiliares, y solo queda validarlos con un "validar fecha" [Capacitación · 18:32](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). En el caso del log, el Forms exigía las dos fechas, desde menor que hasta y no más de 30 días entre ambas [Capacitación · 10:16](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). Si alguna de las dos es nula, error "Debe ingresar fecha desde y fecha hasta" y RETURN [Capacitación · 22:41](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md). Desde mayor que hasta, o más de 30 días, también dan error [Capacitación · 24:18](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- Se cree que, al cargar la primera fecha, el Front copia el valor en la segunda (sin confirmar) [Capacitación · 23:11](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).
- Para una fecha común, desde/hasta queda en el query y es mucho más performante; el caso de la fecha con hora es muy particular [Capacitación · 43:42](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md).

## Contradicciones
Sin contradicciones entre las fuentes.

## Relacionados
- [Validador de campo](termino-validador-de-campo.md)
- [Fecha con hora](caso-fecha-con-hora.md)
- [Campo query](termino-campo-query.md)
- [Case Restriction](termino-case-restriction.md)
- [Títulos de todos los campos](regla-titulos-de-todos-los-campos.md)

## Fuentes
| Video | Fecha | Minuto | Qué aporta |
|---|---|---|---|
| [Capacitación](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md) | 2026-05-12 | 0:02, 0:29, 0:56, 1:25 | Definición, JSON del Front, type y campos auxiliares |
| [Capacitación](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md) | 2026-05-12 | 6:51, 7:43, 8:13, 9:13, 9:41, 10:16, 10:42, 11:09 | Operatoria con campo compuesto; el Front arma el filtro; reglas del caso log |
| [Capacitación](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md) | 2026-05-12 | 12:13, 12:38, 13:11, 13:44, 14:26, 14:57, 15:23, 17:03, 17:58 | "Obtener valores del JSON fecha" y rendimiento |
| [Capacitación](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md) | 2026-05-12 | 18:32, 22:41, 23:11, 24:18 | Validación de las dos fechas |
| [Capacitación](../capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md) | 2026-05-12 | 28:00, 28:30, 29:29, 43:42 | Valida / valida compuesto / no valida; fecha común en el query |
