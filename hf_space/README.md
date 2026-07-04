---
title: Crop Yield Prediction
emoji: 🌾
colorFrom: green
colorTo: yellow
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# Crop Yield Prediction

Docker Space serving a React frontend and FastAPI backend for crop yield
prediction.

The FastAPI service loads the trained model from Hugging Face Model Hub at
startup. The React application is built into static assets and served by the
same FastAPI container.

## Required Space Variables

Set these in the Hugging Face Space settings:

```text
MODEL_SOURCE=hf
HF_MODEL_REPO_ID=YOUR_USERNAME/crop-yield-regressor
HF_MODEL_REVISION=main
APP_ENV=production
API_VERSION=v1.0.0
MODEL_VERSION=v1.0.0
PREDICTION_UNIT=hg/ha
LOG_LEVEL=INFO
CORS_ORIGINS=*
```

If the model repository is private, add this Space secret:

```text
HF_TOKEN=your_huggingface_read_token
```

## Runtime

- React frontend: served from `/`
- FastAPI health endpoint: `/health`
- FastAPI model version endpoint: `/version`
- FastAPI prediction endpoint: `/predict`

## Startup Optimization

The container uses one Uvicorn worker so the model is loaded once per container.
Model files are downloaded through `huggingface_hub` and cached under
`/data/.cache/huggingface`.
