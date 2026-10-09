# wiki_viva

**Wiki viva de consulta de terminología técnica y funcional.** Es un prototipo que convierte transcripciones de reuniones y capacitaciones en una wiki consultable. Sigue el formato [Open Knowledge Format (OKF)](https://agentic-ai.readthedocs.io/en/latest/Standards/open-knowledge-format/) de Google Cloud y la consulta un asistente con dos agentes, uno **funcional** y otro **técnico**.

> **Datos ficticios.** Todo el contenido es inventado a partir de un caso real: personas, empresa, proyecto ("Modernización de módulos"), tablas, claves, tickets, fechas y nombres de archivo. Solo se conservan los conceptos técnicos para que la demo sea creíble: validación compuesta, grupos de negocio, Ref Code, TRUNC, entre otros.

## Qué hace

1. **Arma la wiki.** Las transcripciones automáticas se limpian y se dividen por tema. Cada idea queda con el minuto del video donde se dijo, y se extraen términos, reglas, casos especiales y dudas abiertas. Cada video termina como un documento OKF: Markdown con un encabezado YAML de tipo `Fuente de video`.
2. **Responde consultas** en cuatro pasos:
   - busca los fragmentos relevantes;
   - un agente funcional y uno técnico redactan, en paralelo, afirmaciones apoyadas solo en la wiki;
   - cada minuto citado se verifica contra el documento;
   - se arma la respuesta final, con los tiempos en formato `hh:mm:ss`.

   Si no hay evidencia, la respuesta es exactamente: **«No tengo información sobre tu consulta»**.

## Estructura

```
wiki/                       Bundle OKF (punto de entrada: wiki/index.md)
  index.md                  Índice: videos, temas y rangos de tiempo
  _PLANTILLA_Y_GLOSARIO.md  Formato de los documentos y glosario de jerga / errores de transcripción
  *.md                      Un documento por video (type: Fuente de video)
asistente/
  consulta_okf.py           Motor de búsqueda OKF (Python 3, sin dependencias)
  SKILL.md                  Instrucciones del asistente multiagente (habilidad de Claude)
portal/
  index.html                Portal web de consulta (artifact de claude.ai)
  wiki.json                 Datos del portal, generados desde wiki/
scripts/
  build_wiki_json.py        Regenera portal/wiki.json a partir de wiki/
```

## Uso rápido

```bash
# Regenerar el índice del bundle (después de agregar documentos)
python asistente/consulta_okf.py indexar wiki

# Buscar evidencia para una pregunta (texto legible o --json)
python asistente/consulta_okf.py buscar wiki "¿Cómo se hace la validación compuesta?"
python asistente/consulta_okf.py buscar wiki "¿Qué grupos de negocio existen?" --json

# Regenerar los datos del portal
python scripts/build_wiki_json.py wiki portal/wiki.json
```

El buscador devuelve las secciones y los minutos (`hh:mm:ss`) donde está la respuesta. Las respuestas redactadas por los dos agentes se generan con Claude, siguiendo `asistente/SKILL.md`.

## Portal

`portal/index.html` es un artifact de claude.ai. Usa capacidades propias de esa plataforma: `sample` para los agentes, `db` para guardar las preguntas sin respuesta y las opiniones, y `user`. Por eso, abierto fuera de claude.ai, solo funcionan **Explorar videos** y **Glosario**.

Para consultarlo por fuera de Claude hace falta un backend propio. Ese backend reutilizaría `consulta_okf.py`, haría las tres llamadas a la API de Claude (agente funcional, agente técnico y síntesis) y guardaría la clave de la API del lado del servidor. Es un paso pendiente de este prototipo.

## Formato OKF usado

Cada documento lleva un encabezado YAML. El único campo que exige OKF es `type`; los demás son convenciones de este proyecto:

```yaml
type: Fuente de video
title: ...
description: ...
resource: "Transcripciones/<archivo>.docx"
timestamp: 2026-05-12
duracion: "0:46:00"
participantes: [...]
dominio: funcional | tecnico | ambos
tags: [...]
estado: borrador
calidad_transcripcion: alta | media | baja
```

En el cuerpo, cada idea lleva el minuto entre corchetes (`[m:ss]`). Las reglas van destacadas como `> **Regla:**` y los casos especiales como `> **Caso especial:**`. Los términos que no se pudieron confirmar se marcan con `[?]`.
