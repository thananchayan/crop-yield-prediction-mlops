FROM python:3.10-slim AS builder

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
    APP_NAME="Crop Yield Prediction API" \
    APP_ENV=production \
    API_VERSION=v3.0.0 \
    MODEL_VERSION=v3.0.0 \
    MODEL_SOURCE=local \
    PREDICTION_UNIT=hg/ha \
    LOG_LEVEL=INFO \
    CORS_ORIGINS="http://localhost:5173,http://localhost:3000"

WORKDIR /app

RUN addgroup --system app && \
    adduser --system --ingroup app app

COPY --from=builder /opt/venv /opt/venv

COPY app ./app
COPY ml ./ml

# Copy all artifacts instead of one hardcoded version
COPY artifacts ./artifacts

RUN chown -R app:app /app

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3).read()"

CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]