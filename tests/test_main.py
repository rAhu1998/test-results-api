from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_run():
    res = client.post("/runs" , json ={ "name": "first" , "status" : "pass"})
    data = res.json()
    assert res.status_code == 201
    assert data["name"] == "first"
    assert data["status"] == "pass"
    assert data["id"] == 1

def test_check_health():
    res = client.get("/health")
    data = res.json()
    assert res.status_code == 200
    assert data["health"] == "OK"

def test_create_run_missing_status():
    res = client.post("/runs",json = {"name":"second"})
    data = res.json()
    assert res.status_code == 422
    assert data["detail"][0]["loc"][-1] == "status"
    assert data["detail"][0]["type"] == "missing"
        

def test_create_run_with_id():
    res = client.post("/runs",json = {"id" : 3 ,"name":"third" , "status" : "fail"})
    data = res.json()
    assert res.status_code == 422
    assert data["detail"][0]["loc"][-1] == "id"
    assert data["detail"][0]["type"] == "extra_forbidden"

def test_get_run_with_impossible_id():
    run_id = 999
    res = client.get(f"/runs/{run_id}")
    data = res.json()
    assert res.status_code == 404
    assert data["detail"] == "run_id not found"
