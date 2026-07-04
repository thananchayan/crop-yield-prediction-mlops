# Hugging Face Spaces Deployment

This deployment uses a Docker Space that serves both the React frontend and
FastAPI backend from one container.

## 1. Upload The Model To Model Hub

Replace `YOUR_USERNAME` with your Hugging Face username or organization:

```bash
python3 -m pip install -r requirements-dev.txt
huggingface-cli login
python3 scripts/upload_model_to_hf.py \
  --repo-id YOUR_USERNAME/crop-yield-regressor
```

For a private model repository:

```bash
python3 scripts/upload_model_to_hf.py \
  --repo-id YOUR_USERNAME/crop-yield-regressor \
  --private
```

## 2. Create The Docker Space

Create a new Hugging Face Space with:

```text
SDK: Docker
Visibility: Public or Private
Space name: crop-yield-prediction
```

## 3. Prepare The Space Repository

Copy these project files into the Space repository:

```text
app/
frontend/
requirements.txt
hf_space/Dockerfile
hf_space/README.md
```

In the Space repository root, rename or copy:

```text
hf_space/Dockerfile -> Dockerfile
hf_space/README.md -> README.md
```

## 4. Configure Space Variables

In the Space settings, add:

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

For a private model repository, add a secret:

```text
HF_TOKEN=your_huggingface_read_token
```

## 5. Deploy

Commit and push to the Space repository:

```bash
git add .
git commit -m "Deploy crop yield prediction app"
git push
```

The Space will build the Docker image and start the app on port `7860`.

## 6. Verify

After the Space is running, check:

```text
https://huggingface.co/spaces/YOUR_USERNAME/crop-yield-prediction
https://YOUR_USERNAME-crop-yield-prediction.hf.space/health
https://YOUR_USERNAME-crop-yield-prediction.hf.space/version
```

Send a prediction request:

```bash
curl -X POST https://YOUR_USERNAME-crop-yield-prediction.hf.space/predict \
  -H "Content-Type: application/json" \
  -d '{
    "area": "Albania",
    "item": "Maize",
    "year": 1990,
    "average_rain_fall_mm_per_year": 1485.0,
    "pesticides_tonnes": 121.0,
    "avg_temp": 16.37
  }'
```

## Startup Time Notes

- The Docker image does not include the model artifact, keeping the Space image
  small.
- The model is downloaded from Model Hub once during FastAPI startup.
- `HF_MODEL_CACHE_DIR=/data/.cache/huggingface/hub` allows cached model files to
  be reused when persistent storage is available.
- `--workers 1` avoids loading duplicate model copies.
