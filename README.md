# SmartPipeline AI Web

A real Flask web application for CI log triage, explainable change-risk scoring, and optional LLM-assisted PR diff review.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python app.py
```

Open http://127.0.0.1:5000. Click **Load sample** to try each tool without supplying your own data.

Run tests: `pytest -q`

## Optional LLM

The heuristic analyzer and risk scoring work without a provider. For an OpenAI-compatible endpoint, set:

```bash
export LLM_BASE_URL=http://localhost:11434/v1
export LLM_MODEL=llama3.2:3b
export LLM_API_KEY=ollama
python app.py
```

For local Ollama, install it and pull a model first (`ollama pull llama3.2:3b`). If this app runs in Docker, `localhost` refers to the container, not the host. Hosted provider quotas and free-tier terms can change. Never commit API keys or paste secrets/confidential logs.

## Docker

```bash
docker build -t smartpipeline-ai .
docker run --rm -p 5000:5000 smartpipeline-ai
```

Open http://127.0.0.1:5000. LLM variables are optional.

## API

- `GET /health`
- `POST /api/analyze-log` with `{"log":"..."}`
- `POST /api/risk-score` with `{"paths":["k8s/deployment.yaml"]}`
- `POST /api/review` with `{"diff":"..."}`

## Safety notes

This is a learning starter, not a production security gate. AI output is advisory. Redaction is best-effort; don't submit secrets or confidential code. Before network exposure, add authentication, TLS, rate limiting, stronger secret scanning, and a data-retention policy. Use deterministic tests/scanners and independent human approval for deployments.
