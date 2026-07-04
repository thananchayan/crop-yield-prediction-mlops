FROM node:20-slim AS frontend-builder

WORKDIR /frontend

COPY frontend/package.json ./
RUN npm install

COPY frontend ./
ENV VITE_API_BASE_URL=""
RUN npm run build


FROM python:3.10-slim AS python-builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /build

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


FROM python:3.10-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    APP_NAME="Crop Yield Prediction" \
    APP_ENV=production \
    API_VERSION=v1.0.0 \
    MODEL_VERSION=v1.0.0 \
    MODEL_SOURCE=hf \
    HF_MODEL_REPO_ID="your-username/crop-yield-regressor" \
    HF_MODEL_REVISION=main \
    HF_HOME=/data/.cache/huggingface \
    HF_MODEL_CACHE_DIR=/data/.cache/huggingface/hub \
    FRONTEND_DIST_DIR=/app/frontend/dist \
    PREDICTION_UNIT=hg/ha \
    LOG_LEVEL=INFO \
    CORS_ORIGINS="*"

WORKDIR /app

RUN addgroup --system app && \
    adduser --system --ingroup app app && \
    mkdir -p /data/.cache/huggingface && \
    chown -R app:app /app /data

COPY --from=python-builder /opt/venv /opt/venv
COPY app ./app
COPY --from=frontend-builder /frontend/dist ./frontend/dist

USER app

EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=5s --start-period=45s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:7860/health', timeout=3).read()"

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-7860} --workers 1"]
