from fastapi import FastAPI , HTTPException
from pydantic import BaseModel , ConfigDict
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db
from models import RunModel


class RunIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: str
    name: str

class Run(RunIn):
    id: int
    model_config = ConfigDict(from_attributes=True)

app = FastAPI()

@app.get("/health")
def get_health():
    return {"health":"OK"}

@app.get("/runs",response_model=list[Run])
def get_runs(status :str | None = None, db: Session = Depends(get_db)):
    stmt = select(RunModel)
    if status is None:
        res = db.scalars(stmt).all()
        return res 
    stmt = stmt.where(RunModel.status == status)
    res = db.scalars(stmt).all()
    return res 

@app.get("/runs/{run_id}" , response_model=Run)
def get_run_fromId(run_id : int , db: Session = Depends(get_db)):
    res = db.get(RunModel, run_id)
    if res is None:
        raise HTTPException(status_code=404, detail="run_id not found")
    return res
    
@app.post("/runs", status_code = 201 , response_model=Run)
def post_runs(runIn: RunIn, db: Session = Depends(get_db)):
    run = RunModel(name = runIn.name , status = runIn.status)
    db.add(run)
    db.commit()
    db.refresh(run)
    return run

@app.delete("/runs/{run_id}")
def delete_run_fromId(run_id : int , db: Session = Depends(get_db)):
    res = db.get(RunModel, run_id)
    if res is None:
        raise HTTPException(status_code=404, detail="run_id not found")        
    db.delete(res)
    db.commit()
    return {"Deleted Run for ID" : run_id}
    
@app.put("/runs/{run_id}" , response_model=Run)
def update_onId(run_id : int , runIn : RunIn,  db: Session = Depends(get_db)):
    res = db.get(RunModel, run_id)
    if res is None:
        raise HTTPException(status_code=404, detail="run_id not found")
    res.name , res.status = runIn.name , runIn.status
    db.commit()
    db.refresh(res)
    return res