import pytest

from fastapi.testclient import TestClient
from pytest_httpserver import HTTPServer

from src.app_factory import create_app
from src.container_factory import create_container


# this is needed for non-api based testing
@pytest.fixture(scope="function", autouse=True)
def ctx():
    container = create_container()
    yield container


# session = set up only once for the tests, values are cached
# module = values cached per test file -> module
# default = per function eg. http_client
@pytest.fixture(scope="function")
def fast_api_app(ctx):
    app = create_app()
    yield app


@pytest.fixture
def http_client(fast_api_app):
    with TestClient(fast_api_app) as client:
        yield client


@pytest.fixture(scope="function")
def create_server():
    servers = []

    def _create_server(port):
        server = HTTPServer(port=port)
        server.start()
        servers.append(server)  # Keep track of servers for cleanup
        return server

    yield _create_server

    # Cleanup after tests
    for server in servers:
        server.stop()



