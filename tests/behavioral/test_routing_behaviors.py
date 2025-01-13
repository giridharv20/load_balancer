

def test_register_url_and_basic_routing_with_roundrobin(ctx, http_client, create_server):
    http_server_1 = create_server(port=51000)
    http_server_2 = create_server(port=52000)
    http_server_3 = create_server(port=53000)
    http_servers = [http_server_1, http_server_2, http_server_3]

    ping_mock_response_1 = {'message': 'pong from server 1'}
    ping_mock_response_2 = {'message': 'pong from server 2'}
    ping_mock_response_3 = {'message': 'pong from server 3'}
    ping_mock_responses = [ping_mock_response_1, ping_mock_response_2, ping_mock_response_3]

    for i, http_server in enumerate(http_servers):
        data = {
            "key": "abc",
            "value": http_server.url_for("")
        }
        response = http_client.post("/urls/register_url", json=data)
        assert response.status_code == 200

        http_server.expect_request("/abc/ping").respond_with_json(ping_mock_responses[i])

    response = http_client.get("/abc/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong from server 1"}

    response = http_client.get("/abc/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong from server 2"}

    response = http_client.get("/abc/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong from server 3"}

    response = http_client.get("/abc/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong from server 1"}

    all_servers = ctx.get("UrlService").get_all_servers("abc")
    deregistered_servers = ctx.get("UrlService").get_deregistered_servers("abc")
    unhealthy_servers = ctx.get("UrlService").get_unhealthy_servers("abc")
    assert len(all_servers) == len(http_servers)
    assert deregistered_servers is None
    assert unhealthy_servers is None


def test_register_url_and_roundrobin_with_deregistered_url(ctx, http_client, create_server):
    http_server_1 = create_server(port=51000)
    http_server_2 = create_server(port=52000)
    http_server_3 = create_server(port=53000)
    http_servers = [http_server_1, http_server_2, http_server_3]

    ping_mock_response_1 = {'message': 'pong from server 1'}
    ping_mock_response_2 = {'message': 'pong from server 2'}
    ping_mock_response_3 = {'message': 'pong from server 3'}
    ping_mock_responses = [ping_mock_response_1, ping_mock_response_2, ping_mock_response_3]

    for i, http_server in enumerate(http_servers):
        data = {
            "key": "abc",
            "value": http_server.url_for("")
        }
        response = http_client.post("/urls/register_url", json=data)
        assert response.status_code == 200

        http_server.expect_request("/abc/ping").respond_with_json(ping_mock_responses[i])

    response = http_client.get("/abc/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong from server 1"}

    response = http_client.get("/abc/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong from server 2"}

    data = {
        "key": "abc",
        "value": http_servers[2].url_for("")
    }
    response = http_client.post("/urls/deregister_url", json=data)
    assert response.status_code == 200

    response = http_client.get("/abc/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong from server 1"}

    all_servers = ctx.get("UrlService").get_all_servers("abc")
    deregistered_servers = ctx.get("UrlService").get_deregistered_servers("abc")
    unhealthy_servers = ctx.get("UrlService").get_unhealthy_servers("abc")
    assert len(all_servers) == len(http_servers)
    assert len(deregistered_servers) == 1
    assert unhealthy_servers is None

def test_register_url_and_roundrobin_with_unhealthy_url(ctx, http_client, create_server):
    http_server_1 = create_server(port=51000)
    http_server_2 = create_server(port=52000)
    http_server_3 = create_server(port=53000)
    http_servers = [http_server_1, http_server_2, http_server_3]

    ping_mock_response_1 = {'message': 'pong from server 1'}
    ping_mock_response_2 = {'message': 'pong from server 2'}
    ping_mock_response_3 = {'message': 'pong from server 3'}
    ping_mock_responses = [ping_mock_response_1, ping_mock_response_2, ping_mock_response_3]

    for i, http_server in enumerate(http_servers):
        data = {
            "key": "abc",
            "value": http_server.url_for("")
        }
        response = http_client.post("/urls/register_url", json=data)
        assert response.status_code == 200

        http_server.expect_request("/abc/ping").respond_with_json(ping_mock_responses[i])

    response = http_client.get("/abc/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong from server 1"}

    data = {
        "key": "abc",
        "value": http_servers[1].url_for("")
    }
    response = http_client.post("/urls/unhealthy_url", json=data)
    assert response.status_code == 200

    response = http_client.get("/abc/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong from server 3"}

    response = http_client.get("/abc/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong from server 1"}

    all_servers = ctx.get("UrlService").get_all_servers("abc")
    deregistered_servers = ctx.get("UrlService").get_deregistered_servers("abc")
    unhealthy_servers = ctx.get("UrlService").get_unhealthy_servers("abc")
    assert len(all_servers) == len(http_servers)
    assert deregistered_servers is None
    assert len(unhealthy_servers) == 1
