// Cliente del backend de la Wiki viva. Es el único archivo del frontend que habla con la API.
// Contrato: docs/api/openapi.yaml
//
// Uso:
//   const api = crearApi({ base: "http://localhost:8000", rolDev: "lector" });
//   const res = await api.consultar("¿Qué es un grupo de negocio?", { vista: "ambas", onEtapa: e => ... });

export class ErrorApi extends Error {
  constructor(codigo, mensaje, status) {
    super(mensaje);
    this.codigo = codigo;
    this.status = status;
  }
}

export function crearApi({ base = "", token = null, rolDev = null, usuarioDev = null } = {}) {
  const headers = (extra = {}) => {
    const h = { "Content-Type": "application/json", ...extra };
    if (token) h.Authorization = `Bearer ${typeof token === "function" ? token() : token}`;
    if (rolDev) h["X-Rol-Dev"] = rolDev;          // solo en desarrollo
    if (usuarioDev) h["X-Usuario-Dev"] = usuarioDev;
    return h;
  };

  async function pedir(metodo, ruta, cuerpo) {
    const r = await fetch(base + ruta, { method: metodo, headers: headers(), body: cuerpo ? JSON.stringify(cuerpo) : undefined });
    if (r.status === 204) return null;
    const datos = await r.json().catch(() => null);
    if (!r.ok) throw new ErrorApi(datos?.error?.codigo || "error_interno", datos?.error?.mensaje || r.statusText, r.status);
    return datos;
  }

  // POST /api/consultas con streaming SSE. Llama a onEtapa({etapa, estado}) por cada paso
  // y resuelve con el ResultadoConsulta. Acepta un AbortSignal para detener.
  async function consultar(pregunta, { vista = "ambas", onEtapa = () => {}, signal } = {}) {
    const r = await fetch(base + "/api/consultas", {
      method: "POST", signal,
      headers: headers({ Accept: "text/event-stream" }),
      body: JSON.stringify({ pregunta, vista }),
    });
    if (!r.ok) {
      const datos = await r.json().catch(() => null);
      throw new ErrorApi(datos?.error?.codigo || "error_interno", datos?.error?.mensaje || r.statusText, r.status);
    }
    const lector = r.body.getReader();
    const dec = new TextDecoder();
    let buffer = "";
    for (;;) {
      const { value, done } = await lector.read();
      if (done) break;
      buffer += dec.decode(value, { stream: true });
      let corte;
      while ((corte = buffer.indexOf("\n\n")) >= 0) {
        const bloque = buffer.slice(0, corte);
        buffer = buffer.slice(corte + 2);
        const tipo = (bloque.match(/^event: (.+)$/m) || [])[1];
        const datos = JSON.parse((bloque.match(/^data: (.+)$/m) || [])[1] || "null");
        if (tipo === "etapa") onEtapa(datos);
        else if (tipo === "resultado") return datos;
        else if (tipo === "error") throw new ErrorApi(datos.error.codigo, datos.error.mensaje, 200);
      }
    }
    throw new ErrorApi("error_interno", "La respuesta terminó sin resultado.", 200);
  }

  return {
    salud: () => pedir("GET", "/api/salud"),
    consultar,
    opinar: (consultaId, util, comentario) => pedir("POST", `/api/consultas/${encodeURIComponent(consultaId)}/opinion`, { util, comentario }),
    indice: () => pedir("GET", "/api/wiki/indice"),
    video: (id) => pedir("GET", `/api/wiki/videos/${encodeURIComponent(id)}`),
    glosario: (q = "") => pedir("GET", `/api/glosario${q ? `?q=${encodeURIComponent(q)}` : ""}`),
    huecos: (estado) => pedir("GET", `/api/huecos${estado ? `?estado=${estado}` : ""}`),
    resolverHueco: (id, estado = "resuelta") => pedir("PATCH", `/api/huecos/${encodeURIComponent(id)}`, { estado }),
    linksVideos: () => pedir("GET", "/api/config/videos"),
    guardarLinksVideos: (links) => pedir("PUT", "/api/config/videos", { links }),
  };
}
