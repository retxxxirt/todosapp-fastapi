from requests import Response
from starlette.testclient import TestClient


def make_request(
    client: TestClient,
    method: str,
    path: str,
    data: dict = None,
) -> tuple[Response, dict]:
    """Make request, return response and parsed data"""

    data_key = "params" if method == "get" else "json"
    response = client.request(method, path, **{data_key: data})

    return response, response.json()
