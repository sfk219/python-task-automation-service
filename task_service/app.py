"""Persistent task queue with controlled operation types; learning demo."""
import os,sqlite3,json,uuid
from datetime import datetime,timezone
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from typing import Literal
DB=os.getenv("TASK_DB","tasks.db")
app=FastAPI(title="Task Automation API")
def connect():
    c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
    c.execute("CREATE TABLE IF NOT EXISTS jobs(id TEXT PRIMARY KEY,kind TEXT,payload TEXT,status TEXT,result TEXT,created TEXT)")
    return c
class Task(BaseModel):
    kind:Literal["uppercase","sum","count_words"]
    text:str|None=Field(None,max_length=10000)
    numbers:list[float]|None=None
@app.get("/health")
def health():return {"status":"ok"}
@app.post("/tasks",status_code=201)
def create(task:Task):
    if task.kind=="sum" and (not task.numbers or task.text is not None):raise HTTPException(422,"sum requires numbers")
    if task.kind!="sum" and task.text is None:raise HTTPException(422,"text is required")
    id=str(uuid.uuid4())
    with connect() as db:db.execute("INSERT INTO jobs VALUES(?,?,?,'queued',NULL,?)",(id,task.kind,task.model_dump_json(),datetime.now(timezone.utc).isoformat()))
    return {"id":id,"status":"queued"}
@app.get("/tasks")
def listing():
    with connect() as db:return [dict(r) for r in db.execute("SELECT id,kind,status,created FROM jobs ORDER BY created DESC LIMIT 100")]
@app.get("/tasks/{id}")
def get(id:str):
    with connect() as db:row=db.execute("SELECT * FROM jobs WHERE id=?",(id,)).fetchone()
    if row is None:raise HTTPException(404,"Not found")
    data=dict(row);data["result"]=json.loads(data["result"]) if data["result"] else None;return data
