from fastapi import FastAPI
from pydantic import BaseModel

runs = []

class Runs(BaseModel):
    status : str
    name : str

app = FastAPI()

@app.get("/health")
def get_health():
    return {"health":"OK"}

@app.get("/runs")
def get_runs(status :str | None = None):
    if status is None:
        return { "Runs" : runs}
    else:
        res =[]
        for i in runs:
            if i.status == status:
                res.append(i)
        return { "Runs" : res}

@app.post("/runs", status_code = 201)
def post_runs(run : Runs):
    runs.append(run)
    return run
