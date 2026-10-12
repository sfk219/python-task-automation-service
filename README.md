# Python Task Automation REST Service

A working learning project: FastAPI REST service, persistent SQLite task queue, separate background worker and tests. Only predefined safe operations are supported; user-submitted code is not executed.

## Setup
```bash
python -m venv .venv
# Activate venv, then:
pip install -r requirements-dev.txt
uvicorn task_service.app:app --reload
```
In another terminal, start the background processor:
```bash
python -m task_service.worker
```
Open [http://localhost:8000/docs](http://localhost:8000/docs).

Example:
```bash
curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"kind":"uppercase","text":"hello"}'
```

## Tests
```bash
pytest -q
```

**Tech:** Python, FastAPI, Pydantic, REST APIs, SQLite, async-style background task processing. Single-host demonstration; no production message broker.