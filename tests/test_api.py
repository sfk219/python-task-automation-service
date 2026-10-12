import os,tempfile
from fastapi.testclient import TestClient
from task_service import app as module
def test_queue(monkeypatch):
    with tempfile.TemporaryDirectory() as d:
        monkeypatch.setattr(module,"DB",d+"/tasks.db")
        with TestClient(module.app) as client:
            r=client.post("/tasks",json={"kind":"uppercase","text":"hello"})
            assert r.status_code==201
            ident=r.json()["id"]
            assert module.app.title=="Task Automation API"
            assert client.get("/tasks/"+ident).json()["status"]=="queued"
