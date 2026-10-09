from fastapi import FastAPI , HTTPException
from pydantic import BaseModel , ConfigDict

runs = []
idcount = 1

class RunIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status : str
    name : str

class Runs(RunIn):
        id : int | None = None

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

@app.get("/runs/{run_id}")
def get_run_fromId(run_id : int):
    for i in runs:
        if i.id == run_id:
            return i
    raise HTTPException(status_code=404, detail="run_id not found")

@app.post("/runs", status_code = 201)
def post_runs(runIn : RunIn):
    global idcount
    run = Runs(id=idcount, name=runIn.name, status=runIn.status)
    idcount += 1
    runs.append(run)
    return run

@app.delete("/runs/{run_id}")
def delete_run_fromId(run_id : int):
    for i in runs:
        if i.id ==run_id:
            runs.remove(i)
            return {"Deleted Run for ID" : run_id}
    raise HTTPException(status_code=404, detail="run_id not found")

@app.put("/runs/{run_id}")
def update_onId(run_id : int , runIn : RunIn):
    for i in runs:
        if i.id == run_id:
            i.name = runIn.name
            i.status = runIn.status
            return i
    raise HTTPException(status_code=404, detail="run_id not found")