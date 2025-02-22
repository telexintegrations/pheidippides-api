from tests import client

def test_integration_json():
    response = client.get("/integration.json")
    assert response.status_code == 200
    assert "data" in response.json()