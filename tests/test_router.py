from fastapi.testclient import TestClient

from delivery_api.router import app

client = TestClient(app)


def test_root_path_valid():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_healthcheck_valid():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}