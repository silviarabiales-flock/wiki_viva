---
type: Índice
title: Wiki viva de consulta de terminología técnica y funcional
description: Punto de entrada OKF. Lista las fichas consolidadas y las fuentes (videos procesados) con sus temas y rangos de tiempo, para navegar por divulgación progresiva.
tags: [indice]
---

# Wiki viva de consulta de terminología técnica y funcional

Cómo navegar: empezar por las fichas (reúnen lo dicho en todos los videos sobre un concepto) y,
para el detalle, ir a la fuente y al tema. Glosario de jerga y errores de transcripción:
[_PLANTILLA_Y_GLOSARIO.md](_PLANTILLA_Y_GLOSARIO.md).

## Fichas consolidadas

### Términos

| Ficha | Descripción | Estado | Contradicciones | Última fuente |
|---|---|---|---|---|
| [Campo query (parte del query)](fichas/termino-campo-query.md) | Indicador de la definición de campos que marca si el campo está en el select del query; define si el orden y el filtro los resuelve la base o se hacen después de traer los datos. | borrador | 0 | 2026-05-12 |
| [Case Restriction (formato del campo)](fichas/termino-case-restriction.md) | Propiedad de la definición de campos que, además de mayúsculas/minúsculas, indica el formato con que el Front muestra el dato (MONTO, NUMBER, UPPER, MIXED, LOWER, DATE). | borrador | 0 | 2026-05-12 |
| [Descriptivo y POST-QUERY](fichas/termino-descriptivo-y-post-query.md) | Campo descriptivo es el que muestra la descripción al lado de un código; en Forms se llena en el POST-QUERY y en el sistema nuevo se trae por join o se completa en el paquete. | borrador | 0 | 2026-04-23 |
| [Grupo de negocio](fichas/termino-grupo-de-negocio.md) | Configuración que convierte un campo en un link a otra pantalla (póliza, productor, ingreso, etc.), con su propia clave. | borrador | 0 | 2026-06-16 |
| [Lista de valores (LOV)](fichas/termino-lista-de-valores.md) | Lista que se le muestra al usuario para elegir el valor de un campo; en el sistema nuevo se arma en el paquete con una plantilla, se engancha en "lista genérica" y se declara en la definición del campo (tipo A o S). | borrador | 0 | 2026-04-23 |
| [Ref Code y Record Group](fichas/termino-ref-code-y-record-group.md) | Ref Code es la tabla de códigos/dominios para campos con valores fijos (CG_REF_CODES, sin confirmar); Record Group es el query de Forms que alimenta una LOV. Se usan de forma distinta en la migración. | borrador | 2 | 2026-05-12 |
| [Validador de campo](fichas/termino-validador-de-campo.md) | Procedimiento por campo, armado con la plantilla "validar campo", que valida el dato apenas el usuario lo carga y que se llama desde un único procedimiento "validar registro". | borrador | 0 | 2026-05-12 |
| [Valor compuesto](fichas/termino-valor-compuesto.md) | Campo de filtro (fecha o numérico) que recibe dos valores, desde y hasta, en lugar de uno; el Front arma el filtro y el back solo usa los dos valores para validar. | borrador | 0 | 2026-05-12 |

### Reglas de negocio

| Ficha | Descripción | Estado | Contradicciones | Última fuente |
|---|---|---|---|---|
| [Link con campo nuevo](fichas/regla-link-con-campo-nuevo.md) | Para armar un link a otra pantalla se crea un campo nuevo asociado a un grupo de negocio; no se linkea sobre el campo de la tabla. | borrador | 0 | 2026-06-16 |
| [Pase entre ambientes](fichas/regla-pase-entre-ambientes.md) | Se carga en desa, se pasa a test y, desde test, se genera el script de la parametrización que se manda a prod junto con el paquete y el type. | borrador | 0 | 2026-06-16 |
| [Permisos sobre la tabla migrada y sus relacionadas](fichas/regla-permisos-tablas-relacionadas.md) | Antes de generar hay que dar permisos a la tabla que se migra y a todas las tablas con las que se relaciona; los permisos de pantalla (consulta, edición, borrado) se ajustan aparte. | borrador | 0 | 2026-04-23 |
| [Títulos de todos los campos](fichas/regla-titulos-de-todos-los-campos.md) | Hay que completar el título (label) de todos los campos, como se ven en el Forms, lo antes posible y en la definición, porque después se copia a operatorias, edit e insert. | borrador | 0 | 2026-05-12 |
| [Usuario de auditoría](fichas/regla-usuario-de-auditoria.md) | El usuario que hace la transacción se asigna en el backend antes del insert o update; no se pide, no se modifica ni se muestra en la pantalla. | borrador | 0 | 2026-05-12 |

### Casos especiales

| Ficha | Descripción | Estado | Contradicciones | Última fuente |
|---|---|---|---|---|
| [Fecha con hora](fichas/caso-fecha-con-hora.md) | Cuando la fecha guardada tiene hora, filtrar con TRUNC sobre la columna rompe el índice; lo correcto es ">= desde y < hasta + 1", y la solución provisoria saca el campo del query. | borrador | 0 | 2026-05-12 |
| [Una sola relación por tabla](fichas/caso-una-relacion-por-tabla.md) | El proceso generador relaciona cada tabla una sola vez; si varios campos apuntan a la misma tabla (monedas, Ref Code), uno lleva la relación automática y los demás descriptivos se completan en el paquete. | borrador | 0 | 2026-04-02 |

## Fuentes de video

### [Charla Técnica Modernización de módulos 4](charla-tecnica-modernizacion-modulos-4.md)

- **Fecha:** 2026-04-02 · **Duración:** 1:54:00 · **Dominio:** ambos
- Sesión práctica sobre la migración de la tabla ?XT_ORIGEN_RECAUDO desde Forms al sistema parametrizable, con permisos, Red Code/Ref Code, formatos (Case Restriction), type y paquete, relaciones, campo query, paso 4 de parametrización, vistas, listas de valores y pase de desa a test y a prod.

| # | Tema | Desde | Hasta | Dominio |
|---|---|---|---|---|
| 1 | [Arranque y permisos sobre la tabla migrada y sus relacionadas](charla-tecnica-modernizacion-modulos-4.md#1-arranque-y-permisos-sobre-la-tabla-migrada-y-sus-relacionadas-002-150) | 00:00:02 | 00:01:50 | tecnico |
| 2 | [Descriptivo "esquema" sin datos: LOV, Column Mapping, Record Group y post-query](charla-tecnica-modernizacion-modulos-4.md#2-descriptivo-esquema-sin-datos-lov-column-mapping-record-group-y-post-query-150-850) | 00:01:50 | 00:08:50 | tecnico |
| 3 | [Red Code: nombre, una sola relación por tabla y campos a agregar](charla-tecnica-modernizacion-modulos-4.md#3-red-code-nombre-una-sola-relacion-por-tabla-y-campos-a-agregar-850-1102) | 00:08:50 | 00:11:02 | tecnico |
| 4 | [Alta de campos en la definición: orden, tabla, título, Red Code y sinónimos](charla-tecnica-modernizacion-modulos-4.md#4-alta-de-campos-en-la-definicion-orden-tabla-titulo-red-code-y-sinonimos-1102-1639) | 00:11:02 | 00:16:39 | tecnico |
| 5 | [Grupo de negocio: links a otras pantallas](charla-tecnica-modernizacion-modulos-4.md#5-grupo-de-negocio-links-a-otras-pantallas-1639-1950) | 00:16:39 | 00:19:50 | ambos |
| 6 | [Reordenamiento de campos y Case Restriction como formato (MONTO, NUMBER, UPPER)](charla-tecnica-modernizacion-modulos-4.md#6-reordenamiento-de-campos-y-case-restriction-como-formato-monto-number-upper-1950-2553) | 00:19:50 | 00:25:53 | tecnico |
| 7 | [Agregado de los descriptivos faltantes](charla-tecnica-modernizacion-modulos-4.md#7-agregado-de-los-descriptivos-faltantes-2553-2933) | 00:25:53 | 00:29:33 | tecnico |
| 8 | [Títulos por defecto y diseño: Forms frente a grilla y vistas](charla-tecnica-modernizacion-modulos-4.md#8-titulos-por-defecto-y-diseno-forms-frente-a-grilla-y-vistas-2933-3846) | 00:29:33 | 00:38:46 | ambos |
| 9 | [Alcance: tablas satélite de configuración y pantalla ABM](charla-tecnica-modernizacion-modulos-4.md#9-alcance-tablas-satelite-de-configuracion-y-pantalla-abm-3846-4137) | 00:38:46 | 00:41:37 | ambos |
| 10 | [Estado de la carga, number/monto y lo que falta (type, paquete, paso 4)](charla-tecnica-modernizacion-modulos-4.md#10-estado-de-la-carga-numbermonto-y-lo-que-falta-type-paquete-paso-4-4137-4910) | 00:41:37 | 00:49:10 | tecnico |
| 11 | [Generación del type y del paquete (pasos 2 y 3)](charla-tecnica-modernizacion-modulos-4.md#11-generacion-del-type-y-del-paquete-pasos-2-y-3-4910-5251) | 00:49:10 | 00:52:51 | tecnico |
| 12 | [Armado de relaciones (join) en el paquete: dominio y low value](charla-tecnica-modernizacion-modulos-4.md#12-armado-de-relaciones-join-en-el-paquete-dominio-y-low-value-5251-5741) | 00:52:51 | 00:57:41 | tecnico |
| 13 | [Completar descriptivos en el paquete copiando el código del Forms](charla-tecnica-modernizacion-modulos-4.md#13-completar-descriptivos-en-el-paquete-copiando-el-codigo-del-forms-5741-10716) | 00:57:41 | 01:07:16 | tecnico |
| 14 | [Prueba del paquete: list type y asignación al type](charla-tecnica-modernizacion-modulos-4.md#14-prueba-del-paquete-list-type-y-asignacion-al-type-10716-11609) | 01:07:16 | 01:16:09 | tecnico |
| 15 | [Campo query y performance de orden y filtro](charla-tecnica-modernizacion-modulos-4.md#15-campo-query-y-performance-de-orden-y-filtro-11609-12055) | 01:16:09 | 01:20:55 | tecnico |
| 16 | [Paso 4: parametrización de consulta, grilla e insert; operatoria, vistas y permisos](charla-tecnica-modernizacion-modulos-4.md#16-paso-4-parametrizacion-de-consulta-grilla-e-insert-operatoria-vistas-y-permisos-12055-12800) | 01:20:55 | 01:28:00 | ambos |
| 17 | [Listas de valores en el paquete: plantilla, lista genérica y definición](charla-tecnica-modernizacion-modulos-4.md#17-listas-de-valores-en-el-paquete-plantilla-lista-generica-y-definicion-12800-14436) | 01:28:00 | 01:44:36 | tecnico |
| 18 | [Edición, pre-update, borrado y tarea para la próxima](charla-tecnica-modernizacion-modulos-4.md#18-edicion-pre-update-borrado-y-tarea-para-la-proxima-14436-14723) | 01:44:36 | 01:47:23 | ambos |
| 19 | [Paso 5: operatoria auxiliar (tablas padre/hija)](charla-tecnica-modernizacion-modulos-4.md#19-paso-5-operatoria-auxiliar-tablas-padrehija-14723-14910) | 01:47:23 | 01:49:10 | tecnico |
| 20 | [Pase de desa a test y a prod: script de migración de la parametrización](charla-tecnica-modernizacion-modulos-4.md#20-pase-de-desa-a-test-y-a-prod-script-de-migracion-de-la-parametrizacion-14910-15351) | 01:49:10 | 01:53:51 | tecnico |

### [Charla Técnica Modernización de módulos 6 — Usuario de auditoría, validadores por campo y validación de póliza](charla-tecnica-modernizacion-modulos-6.md)

- **Fecha:** 2026-04-23 · **Duración:** 0:42:30 · **Dominio:** tecnico
- Sesión de revisión sobre una pantalla migrada desde Forms (ramo/póliza/certificado, saldo, estado). Se discute dónde asignar el usuario que hace la transacción en el insert y cómo armar validadores por campo (plantilla "validar campo" llamada desde un único procedimiento "validar registro") que robustecen la validación de póliza, estatus y saldo.

| # | Tema | Desde | Hasta | Dominio |
|---|---|---|---|---|
| 1 | [Usuario de auditoría en insert/update: comportamiento del Forms](charla-tecnica-modernizacion-modulos-6.md#1-usuario-de-auditoria-en-insertupdate-comportamiento-del-forms-002-513) | 00:00:02 | 00:05:13 | tecnico |
| 2 | [Dónde asignar el usuario: validación pre-insert vs. insert](charla-tecnica-modernizacion-modulos-6.md#2-donde-asignar-el-usuario-validacion-pre-insert-vs-insert-513-836) | 00:05:13 | 00:08:36 | tecnico |
| 3 | [Saldo y productor (se saca el productor)](charla-tecnica-modernizacion-modulos-6.md#3-saldo-y-productor-se-saca-el-productor-836-928) | 00:08:36 | 00:09:28 | ambos |
| 4 | [Validaciones del alta y el POST-CHANGE del certificado en el Forms](charla-tecnica-modernizacion-modulos-6.md#4-validaciones-del-alta-y-el-post-change-del-certificado-en-el-forms-928-1350) | 00:09:28 | 00:13:50 | tecnico |
| 5 | [Procedimiento único "validar registro" y plantilla "validar campo"](charla-tecnica-modernizacion-modulos-6.md#5-procedimiento-unico-validar-registro-y-plantilla-validar-campo-1350-2003) | 00:13:50 | 00:20:03 | tecnico |
| 6 | [Validar desde ramo, póliza y certificado: navegación entre campos](charla-tecnica-modernizacion-modulos-6.md#6-validar-desde-ramo-poliza-y-certificado-navegacion-entre-campos-2003-2451) | 00:20:03 | 00:24:51 | tecnico |
| 7 | [Campo Estado: descriptivo, validate vs. lista de valores, POST-QUERY](charla-tecnica-modernizacion-modulos-6.md#7-campo-estado-descriptivo-validate-vs-lista-de-valores-post-query-2451-3052) | 00:24:51 | 00:30:52 | tecnico |
| 8 | [Llamada desde validar registro y nombres de campo](charla-tecnica-modernizacion-modulos-6.md#8-llamada-desde-validar-registro-y-nombres-de-campo-3052-3213) | 00:30:52 | 00:32:13 | tecnico |
| 9 | [Procedimiento común de póliza: existencia, estatus, saldo, NO_DATA_FOUND](charla-tecnica-modernizacion-modulos-6.md#9-procedimiento-comun-de-poliza-existencia-estatus-saldo-nodatafound-3213-3909) | 00:32:13 | 00:39:09 | ambos |
| 10 | [Cierre: criterios generales, reutilización en update y tarea](charla-tecnica-modernizacion-modulos-6.md#10-cierre-criterios-generales-reutilizacion-en-update-y-tarea-3909-4230) | 00:39:09 | 00:42:30 | tecnico |

### [Capacitación: validación compuesta – campo fecha (12/05/2026)](capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md)

- **Fecha:** 2026-05-12 · **Duración:** 0:46:00 · **Dominio:** tecnico
- Cómo manejar un filtro de fecha compuesto (fecha desde/hasta) en una pantalla migrada desde Forms. Cubre campos auxiliares, la lectura del JSON en el type, el validador de fechas y el problema de rendimiento cuando la fecha tiene hora (TRUNC frente a ">= desde y < hasta + 1").

| # | Tema | Desde | Hasta | Dominio |
|---|---|---|---|---|
| 1 | [Valores compuestos: JSON del Front, type y campos auxiliares](capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md#1-valores-compuestos-json-del-front-type-y-campos-auxiliares-002-359) | 00:00:02 | 00:03:59 | tecnico |
| 2 | [Análisis del Forms: WHERE del bloque y operatoria con fecha compuesta](capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md#2-analisis-del-forms-where-del-bloque-y-operatoria-con-fecha-compuesta-651-1042) | 00:06:51 | 00:10:42 | tecnico |
| 3 | [Asignación JSON → type: "obtener valores del JSON fecha"](capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md#3-asignacion-json-type-obtener-valores-del-json-fecha-1042-1832) | 00:10:42 | 00:18:32 | tecnico |
| 4 | [Validador de fecha: formato, RETURN y reglas](capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md#4-validador-de-fecha-formato-return-y-reglas-1832-2443) | 00:18:32 | 00:24:43 | tecnico |
| 5 | [Validadores que modifican otros campos](capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md#5-validadores-que-modifican-otros-campos-2443-2800) | 00:24:43 | 00:28:00 | tecnico |
| 6 | [Parametrización del filtro: valida, valida compuesto y no valida](capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md#6-parametrizacion-del-filtro-valida-valida-compuesto-y-no-valida-2800-2954) | 00:28:00 | 00:29:54 | tecnico |
| 7 | [Fecha con hora: TRUNC, índices y campo fuera del query](capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md#7-fecha-con-hora-trunc-indices-y-campo-fuera-del-query-2954-4113) | 00:29:54 | 00:41:13 | tecnico |
| 8 | [Marcar el campo como no query, Case Restriction, títulos y tarea](capacitacion-validacion-compuesta-campo-fecha-2026-05-12.md#8-marcar-el-campo-como-no-query-case-restriction-titulos-y-tarea-4113-4506) | 00:41:13 | 00:45:06 | tecnico |

### [Modernización de módulos – Revisión de avance (16/06/2026)](modernizacion-modulos-revision-avance-2026-06-16.md)

- **Fecha:** 2026-06-16 · **Duración:** 0:08:49 · **Dominio:** ambos
- Explicación de cómo se arma un link a otra pantalla mediante "grupos de negocio" (póliza, productor, ingreso, etc.) y cómo pedir grupos nuevos; cierre con scripts pendientes de ejecutar.

| # | Tema | Desde | Hasta | Dominio |
|---|---|---|---|---|
| 1 | [Cómo funciona el link "ver póliza" con grupo de negocio](modernizacion-modulos-revision-avance-2026-06-16.md#1-como-funciona-el-link-ver-poliza-con-grupo-de-negocio-018-239) | 00:00:18 | 00:02:39 | ambos |
| 2 | [Grupos de negocio existentes y cómo pedir uno nuevo](modernizacion-modulos-revision-avance-2026-06-16.md#2-grupos-de-negocio-existentes-y-como-pedir-uno-nuevo-258-724) | 00:02:58 | 00:07:24 | ambos |
| 3 | [Scripts pendientes y URL del ticket 4318](modernizacion-modulos-revision-avance-2026-06-16.md#3-scripts-pendientes-y-url-del-ticket-4318-735-843) | 00:07:35 | 00:08:43 | tecnico |
