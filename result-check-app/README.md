# Result-Check App — CI/CD Pipeline Demo

A student result-check web application with a complete GitHub Actions CI/CD pipeline.

## 🌐 Live App

Students enter their roll number (101–110) to view exam marks, grade, and pass/fail status.

## 🔧 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11 + Flask 3.1 |
| Testing | pytest 8.3.5 + pytest-cov |
| Container | Docker (python:3.11-slim) |
| CI/CD | GitHub Actions (4 stages) |
| Registry | Docker Hub |

## 📁 Project Structure

```
result-check-app/
├── .github/
│   └── workflows/
│       └── ci-cd.yml        ← GitHub Actions pipeline (4 stages)
├── templates/
│   ├── index.html           ← Home page (roll number form)
│   └── result.html          ← Result display page
├── static/
│   └── style.css            ← Dark glassmorphism UI
├── tests/
│   ├── __init__.py
│   ├── test_results.py      ← 31 unit & integration tests ✅
│   └── test_results_broken.py ← Intentional failure demo ❌
├── app.py                   ← Flask application
├── results.py               ← Result data & lookup logic
├── conftest.py              ← pytest path configuration
├── requirements.txt         ← flask, pytest, pytest-cov
├── Dockerfile               ← Container definition
└── .dockerignore
```

## 🚀 Pipeline Stages

```
git push → [test] → [build-image] → [push-to-hub] → [deploy]
```

Each stage only runs if the previous one passes.

| Stage | Action | Blocks on failure? |
|-------|--------|-------------------|
| 1. test | Run 31 pytest unit tests | ✅ Yes — stops everything |
| 2. build-image | Docker build | ✅ Yes |
| 3. push-to-hub | Push to Docker Hub | ✅ Yes |
| 4. deploy | Run container + health check | — |

## 🏃 Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/test_results.py -v

# Run with coverage
pytest tests/test_results.py -v --cov=. --cov-report=term-missing

# Start app
python app.py
# Open http://127.0.0.1:5000
```

## 🐋 Run with Docker

```bash
docker build -t result-check-app .
docker run -d -p 5000:5000 --name result-check result-check-app
# Open http://localhost:5000
```

## 🔐 GitHub Secrets Required

Set these in your GitHub repo → Settings → Secrets → Actions:

| Secret | Value |
|--------|-------|
| `DOCKER_USERNAME` | Your Docker Hub username |
| `DOCKER_PASSWORD` | Your Docker Hub access token |

## 🧪 Demo: Intentional Pipeline Failure

To demonstrate the pipeline stops when tests fail:

1. In `ci-cd.yml`, change the test command to run `test_results_broken.py`
2. Push to GitHub
3. Observe: Stage 1 fails → Stages 2, 3, 4 are all **skipped**
4. Revert to `test_results.py` → pipeline is green again

## 📊 Test Results

```
31 passed in 0.56s
Coverage: 92%
  app.py:     95%
  results.py: 100%
```

## 🎓 Course End Project

- **Subject**: DevOps Engineering
- **Topic**: CI/CD Pipeline with GitHub Actions
- **Level**: L4 (Analyze) + L5 (Evaluate)
