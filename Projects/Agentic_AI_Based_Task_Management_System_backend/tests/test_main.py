import pytest
from fastapi.testclient import TestClient


def test_read_main(client: TestClient):
    response = client.get("/")
    assert response.status_code == 404  # Since we removed the root endpoint


def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 404  # Since we removed the health endpoint