

def test_ping_api(http_client):
    response = http_client.get("/urls/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}
