"""Worker: python -m task_service.worker"""
from .app import connect
import json,time,os
def once():
    with connect() as db:
        row=db.execute("SELECT id,kind,payload FROM jobs WHERE status='queued' ORDER BY created LIMIT 1").fetchone()
        if row is None:return False
        payload=json.loads(row["payload"])
        if row["kind"]=="sum": result={"sum":sum(payload["numbers"])}
        elif row["kind"]=="uppercase":result={"text":payload["text"].upper()}
        else:result={"words":len(payload["text"].split())}
        db.execute("UPDATE jobs SET status='completed',result=? WHERE id=?",(json.dumps(result),row["id"]))
    return True
if __name__=="__main__":
    while True:
        if not once():time.sleep(1)
