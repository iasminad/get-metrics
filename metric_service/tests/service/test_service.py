import json
import pytest
import service as app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        app.latest_data.clear()
        yield client


def test_receive_post(client):
    payload = {
        "CPU": 4,
        "Virtual Memory": 8000000000,
        "Used RAM": 66.5,
        "Memory Left": 33.5
    }
    response = client.post("/receive", data=json.dumps(payload),
                           content_type='application/json')
    assert response.status_code == 200
    assert response.get_json() == payload
    assert app.latest_data[-1] == payload


def test_show_data_with_content(client):
    app.latest_data.append({"CPU": 1}) 
    response = client.get("/show")
    assert response.status_code == 200
    data = response.get_json()
    assert "Data" in data
    assert isinstance(data["Data"], list)
    assert data["Data"][0]["CPU"] == 1


def test_show_data_without_content(client):
    response = client.get("/show")
    assert response.status_code == 200
    assert response.get_json() == {"message": "No data received yet"}


def test_metrics_returns_prometheus_format(client):
    app.latest_data.append({
        "CPU": 2,
        "Virtual Memory": 1234567890,
        "Used RAM": 70.0,
        "Memory Left": 30.0
    })

    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.content_type == "text/plain; version=0.0.4; charset=utf-8"
    body = response.data.decode()

    assert "system_cpu_usage" in body
    assert "system_used_ram" in body
