from entities.service_url_list_type import Service_Url_List_Type
from src.services.health_check.health_checker import HealthCheck


def test_health_checker_all_servers_good(ctx, http_client, create_server):
    http_server_1 = create_server(port=51000)
    http_server_2 = create_server(port=52000)
    http_servers = [http_server_1, http_server_2]

    for http_server in http_servers:
        data = {
            "key": "abc",
            "value": http_server.url_for("")
        }
        response = http_client.post("/urls/register_url", json=data)
        assert response.status_code == 200

    mock_response_1 = {'message': 'pong from server 1'}
    mock_response_2 = {'message': 'pong from server 2'}
    http_server_1.expect_request("/abc/ping").respond_with_json(mock_response_1)
    http_server_2.expect_request("/abc/ping").respond_with_json(mock_response_2)

    system_under_test = HealthCheck(ctx)
    system_under_test.run_health_checker()

    assert len(ctx.get(Service_Url_List_Type.All_Service_Urls.name).get("abc")) == 2
    assert ctx.get(Service_Url_List_Type.Unhealthy_Service_Urls.name).get("abc") is None
    assert ctx.get(Service_Url_List_Type.Deregistered_Service_Urls.name).get("abc") is None


def test_health_checker_where_one_server_is_unavailable(ctx, http_client, create_server):
    http_server_1 = create_server(port=51000)
    http_server_2 = create_server(port=52000)
    http_servers = [http_server_1, http_server_2]

    for http_server in http_servers:
        data = {
            "key": "abc",
            "value": http_server.url_for("")
        }
        response = http_client.post("/urls/register_url", json=data)
        assert response.status_code == 200

    mock_response_1 = {'message': 'pong from server 1'}
    mock_response_2 = {'message': 'service unavailable'}
    http_server_1.expect_request("/abc/ping").respond_with_json(mock_response_1)
    http_server_2.expect_request("/abc/ping").respond_with_json(mock_response_2, status=503)

    system_under_test = HealthCheck(ctx)
    system_under_test.run_health_checker()

    assert len(ctx.get(Service_Url_List_Type.All_Service_Urls.name).get("abc")) == 2
    assert len(ctx.get(Service_Url_List_Type.Unhealthy_Service_Urls.name).get("abc")) == 1
    assert ctx.get(Service_Url_List_Type.Deregistered_Service_Urls.name).get("abc") is None