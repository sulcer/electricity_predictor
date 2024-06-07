# ⚡ Electricity Predictor

## Overview
Electricity Predictor is a machine learning project designed to forecast electricity prices and production in Slovenia. It leverages advanced Recurrent Neural Networks (RNNs), specifically Gated Recurrent Units (GRUs) and Bidirectional GRUs, for accurate predictions. The project also provides insights into the production of various energy sources, including hydro, fossil, nuclear, and cross-border trading.

## Features
- **Electricity Price Prediction**: Forecasts the next 24 hours of electricity prices for the following day.
- **Energy Production Prediction**: Predicts daily production levels for hydro, fossil, nuclear, and cross-border trading.
- **Data Validation**: Includes data validation using GX and Evidently.
- **Model Evaluation**: Daily evaluation using KS tests and custom reports.
- **Model Compression**: Utilizes quantization for model compression.
- **Training Enhancements**: Implements learning rate reduction and early stopping.
- **Data and Experiment Tracking**: Uses DVC for data versioning and MLflow for experiment tracking.
- **Model Deployment**: Models are converted to ONNX format and served using ONNX Runtime.
- **Server**: Written in FastAPI, exposing models and latest data via API endpoints.
- **Client**: Built with Next.js, offering an interactive UI/UX and an extended admin dashboard. Uses React Query for efficient API calls and caching.
- **CI/CD**: Fully automated CI/CD pipelines for server and client deployment, data fetching.

## Technologies Used

### Dependencies
- **Python**: ^3.12
- **Pandas**: ^2.2.1
- **Scikit-learn**: ^1.4.1.post1
- **FastAPI**: ^0.110.0
- **Uvicorn**: {extras = ["standard"], version = "^0.28.0"}
- **Pytest**: ^8.1.1
- **Jupyter**: ^1.0.0
- **Numpy**: ^1.26.4
- **Seaborn**: ^0.13.2
- **TensorFlow**: ^2.15.0.post1
- **Requests**: ^2.31.0
- **SciPy**: ^1.12.0
- **Poe the Poet**: ^0.25.0
- **Pydantic Settings**: ^2.2.1
- **Great Expectations**: ^0.18.12
- **Evidently**: ^0.4.19
- **MLflow**: ^2.12.1
- **Dagshub**: ^0.3.24
- **tf2onnx**: ^1.16.1
- **ONNX Runtime**: ^1.17.3
- **TF-Keras**: ^2.16.0
- **TensorFlow Model Optimization**: ^0.8.0
- **Cachetools**: ^5.3.3
- **PyMongo**: ^4.7.2
- **APScheduler**: ^3.10.4

### Development Dependencies
- **Ruff**: ^0.3.2
- **Black**: ^24.4.0
- **Jupyter**: ^1.0.0

### Modeling
- **Models**: Uses GRU and Bidirectional GRU architectures.
- **ONNX Format**: Models are converted to ONNX format for efficient deployment.
- **Quantization**: Applied to reduce model size and improve inference speed.
- **Learning Rate Reduction and Early Stopping**: Implemented to enhance training efficiency.

### Data Management
- **Data Version Control (DVC)**: Manages datasets and tracks changes.
- **MLflow**: Tracks experiments, models, and daily evaluations.

### Server
- **FastAPI**: Serves the models and provides API endpoints for the latest data.
- **Cron Jobs**: Automates daily tasks such as model registry updates and predictions.

### Client
- **Next.js**: Provides a modern, interactive UI/UX.
- **React Query**: Handles API calls and caching.

### Continuous Integration and Deployment
- **CI/CD**: Automated pipelines for server and client deployment on every push.
- **GitHub Actions**: Executes validation scripts and deploys changes to production.

## Poe Tasks

### Task Definitions
- **serve**: `uvicorn src.serve.main:app --reload`
- **fetch**: `python3 -m src.data.fetch`
- **process**: `python3 -m src.data.process`
- **validate**: `python3 -m src.data.validation.run_checkpoint`
- **data_drift**: `python3 -m src.data.validation.data_drift`
- **stability_tests**: `python3 -m src.data.validation.stability_tests`
- **ks_test**: `python3 -m src.data.validation.ks`
- **lint**: `ruff check .`
- **test**: `pytest src/serve/`
- **train**: `python3 -m src.models.train_model`
- **predict**: `python3 -m src.models.predict_model`
- **validate_predictions**: `python3 -m src.data.validation.validate_predictions`
