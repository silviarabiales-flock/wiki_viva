# Backend – Wiki viva

API que separa la lógica del portal. El backend lee la wiki OKF, busca, corre los agentes y verifica los minutos citados. El frontend solo muestra lo que recibe.

- **Contrato:** [`docs/api/openapi.yaml`](../docs/api/openapi.yaml). Con el backend levantado, la documentación interactiva está en `http://localhost:8000/docs`.
- **Estado:** fases 1 y 2. Los agentes funcionan en **modo simulación**: son deterministas, no llaman a la API de Claude y no tienen costo. Sirven para probar la comunicación completa.

## Cómo se comunican

```
frontend/api.js ──HTTPS + token──▶ /api/...  (FastAPI)
                ◀──JSON o SSE────
```

`POST /api/consultas` con `Accept: text/event-stream` devuelve los eventos a medida que avanza la consulta:

```
event: etapa     data: {"etapa":"busqueda","estado":"en_curso"}
event: etapa     data: {"etapa":"busqueda","estado":"listo"}
event: etapa     data: {"etapa":"funcional","estado":"en_curso"}
event: etapa     data: {"etapa":"tecnico","estado":"en_curso"}
event: etapa     data: {"etapa":"tecnico","estado":"listo"}
event: etapa     data: {"etapa":"funcional","estado":"listo"}
event: etapa     data: {"etapa":"verificacion","estado":"listo"}
event: etapa     data: {"etapa":"sintesis","estado":"listo"}
event: resultado data: {"consulta_id":"c_…","sin_informacion":false,"respuesta":"… [T1]","citas":[{"id":"T1","minuto":"00:09:41",…}]}
```

Con `Accept: application/json` llega directamente el resultado final. Si no hay evidencia, la respuesta es `"No tengo información sobre tu consulta"` y la pregunta queda registrada en `/api/huecos`.

## Flujo interno de una consulta

```
pregunta → búsqueda BM25 (asistente/consulta_okf.py)
         → sin resultados: reformula con el glosario y reintenta → sin resultados: "No tengo información…"
         → agentes funcional y técnico en paralelo (simulación hoy; Claude en la fase 3)
         → verificación: descarta toda afirmación cuyo minuto no exista en el documento
         → síntesis con referencias [F1]/[T1] → guarda la consulta → responde
```

| Módulo | Qué hace |
|---|---|
| `app/main.py` | Endpoints, CORS, streaming SSE |
| `app/motor/wiki.py` | Carga el bundle OKF en memoria, glosario, búsqueda y contexto para los agentes |
| `app/agentes/base.py` | Interfaz común de los agentes (simulación y Claude) |
| `app/agentes/simulacion.py` | Agentes de prueba, sin API |
| `app/agentes/claude.py` | Agentes reales (fase 3, pendiente) |
| `app/agentes/orquestador.py` | Etapas, verificación de minutos, armado del resultado |
| `app/datos/repositorio.py` | SQLite: consultas, preguntas sin respuesta, opiniones, links de grabaciones |
| `app/seguridad.py` | Roles (`lector` < `colaborador` < `editor`) y límite de consultas por minuto |

## Levantarlo

**Con Docker** (desde la raíz del repo):

```bash
docker compose up --build
# API:  http://localhost:8000/docs
# Demo: http://localhost:8080/demo.html
```

**Sin Docker:**

```bash
cd backend
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8000
# en otra terminal, para la demo:
cd frontend && python -m http.server 8080
```

**Probar con curl:**

```bash
curl -s localhost:8000/api/salud
curl -s -X POST localhost:8000/api/consultas -H 'Content-Type: application/json' \
     -d '{"pregunta":"¿Qué es un grupo de negocio?"}'
curl -sN -X POST localhost:8000/api/consultas -H 'Accept: text/event-stream' -H 'Content-Type: application/json' \
     -d '{"pregunta":"¿Cómo se hace la validación compuesta?"}'
# acciones de editor en desarrollo:
curl -s -X PUT localhost:8000/api/config/videos -H 'X-Rol-Dev: editor' -H 'Content-Type: application/json' \
     -d '{"links":{"capacitacion-validacion-compuesta-campo-fecha-2026-05-12":"https://empresa.sharepoint.com/..."}}'
```

**Tests** (contrato y preguntas de control):

```bash
cd backend && pytest -q
```

Los tests validan cada respuesta contra los esquemas del contrato OpenAPI. Además comprueban:

- que «¿Cómo se hace la validación compuesta?» responda con minutos que existen en el documento;
- que una pregunta fuera de la wiki devuelva "No tengo información sobre tu consulta" y quede registrada;
- el orden de los eventos SSE;
- los roles, el límite de consultas y los links al segundo exacto de la grabación.

## Configuración

| Variable | Por defecto | Uso |
|---|---|---|
| `MODO_AGENTES` | `simulacion` | `claude` desde la fase 3 |
| `ANTHROPIC_API_KEY` | — | Clave de la API (fase 3). Solo en el servidor, como secreto |
| `MODELO_AGENTES`, `MODELO_SINTESIS` | — | Modelos de los agentes y de la síntesis (fase 3) |
| `AUTH_MODO` | `desarrollo` | `entra` desde la fase 5 (token de Microsoft Entra ID) |
| `ROL_DEV_POR_DEFECTO` | `lector` | En desarrollo, el rol se cambia con el header `X-Rol-Dev` |
| `ORIGENES_PERMITIDOS` | `http://localhost:5173,http://localhost:8080` | CORS |
| `CONSULTAS_POR_MINUTO` | `20` | Límite por usuario |
| `WIKI_DIR`, `ASISTENTE_DIR`, `DB_PATH` | rutas del repo | Ubicación de la wiki, del motor y de la base |
| `SIMULACION_DEMORA_MS` | `0` | Pausa por etapa en simulación, para ver el avance |

## Próximas fases

3. **Agentes con Claude:** implementar `app/agentes/claude.py` con los prompts de `asistente/SKILL.md`. La interfaz y la verificación ya están, así que no cambia nada más.
4. **Frontend:** adaptar `portal/index.html` para que use `frontend/api.js` en lugar de las capacidades de claude.ai.
5. **Seguridad y datos:** inicio de sesión con Microsoft Entra ID (`AUTH_MODO=entra`), roles desde el token y Postgres si va a producción.
6. **Despliegue:** Azure y publicación automática cuando cambie `wiki/`.
