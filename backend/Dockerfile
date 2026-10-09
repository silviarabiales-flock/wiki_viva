# Se construye desde la raíz del repo: docker build -f backend/Dockerfile .
FROM python:3.12-slim
WORKDIR /srv
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt
COPY asistente/ asistente/
COPY wiki/ wiki/
COPY backend/app/ backend/app/
WORKDIR /srv/backend
ENV WIKI_DIR=/srv/wiki ASISTENTE_DIR=/srv/asistente DB_PATH=/data/wiki_viva.db
RUN mkdir -p /data
VOLUME /data
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
