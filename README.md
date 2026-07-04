# 🌾 Crop Yield Prediction -- Production-Ready ML API with MLOps

An end-to-end Machine Learning project that predicts agricultural crop
yield using a production-ready MLOps workflow. This project demonstrates
how an ML model can be trained, versioned, tested, containerized,
deployed, and served through a REST API with a modern web frontend.

## 🚀 Live Demo

-   **Frontend (Hugging Face Space):**
    https://thananchayan-crop-yield-prediction.hf.space/index.html
-   **Model Hub:**
    https://huggingface.co/thananchayan/crop-yield-regressor

## ✨ Features

-   Machine Learning model for crop yield prediction
-   FastAPI REST API
-   React + TypeScript frontend
-   Model versioning
-   GitFlow workflow
-   Pull Request based development
-   GitHub Actions CI pipeline
-   Ruff linting
-   Black formatting
-   Pytest unit tests
-   Docker containerization
-   Hugging Face Model Hub integration
-   Hugging Face Spaces deployment
-   Environment-based configuration

## 🛠️ Tech Stack

### Machine Learning

-   Python
-   Scikit-learn
-   Pandas
-   NumPy
-   Joblib

### Backend

-   FastAPI
-   Pydantic
-   Uvicorn

### Frontend

-   React
-   TypeScript
-   Vite

### DevOps & MLOps

-   Git & GitHub
-   GitHub Actions
-   Docker
-   Hugging Face Model Hub
-   Hugging Face Spaces

## 📂 Project Structure

``` text
.
├── app/
├── frontend/
├── ml/
├── scripts/
├── tests/
├── artifacts/
├── Dockerfile
├── docker-compose.yml
└── .github/workflows/
```

## 🔄 MLOps Workflow

1.  Create a feature branch.
2.  Train the model and generate versioned artifacts.
3.  Run Ruff, Black and Pytest locally.
4.  Open a Pull Request.
5.  GitHub Actions validates code quality and Docker build.
6.  Merge changes.
7.  Upload the model to Hugging Face Model Hub.
8.  Deploy the application to Hugging Face Spaces.

## 📊 API Endpoints

  Method   Endpoint     Description
  -------- ------------ --------------------
  GET      `/`          API information
  GET      `/health`    Health check
  GET      `/version`   Model version
  POST     `/predict`   Predict crop yield

## ▶️ Run Locally

``` bash
git clone <repository-url>
cd crop-yield-prediction-mlops

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
pip install -r requirements-dev.txt

uvicorn app.main:app --reload
```

Frontend:

``` bash
cd frontend
npm install
npm run dev
```

Run tests:

``` bash
python -m pytest
```

## 📦 Deployment

-   Docker
-   GitHub Actions
-   Hugging Face Model Hub
-   Hugging Face Spaces

## 🎯 Skills Demonstrated

-   Production-ready ML APIs
-   MLOps
-   CI/CD
-   GitFlow
-   Model Versioning
-   Docker
-   FastAPI
-   React
-   Hugging Face
