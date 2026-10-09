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