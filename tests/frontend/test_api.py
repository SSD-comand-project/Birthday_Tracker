from app.frontend.api import handle_response
from unittest.mock import MagicMock


def test_handle_response_success():
    response = MagicMock()
    response.ok = True
    response.json.return_value = {"data": 123}

    result = handle_response(response)

    assert result == {"data": 123}


def test_handle_response_401(monkeypatch):
    response = MagicMock()
    response.status_code = 401
    response.ok = False
    response.json.return_value = {"detail": "Unauthorized"}

    result = handle_response(response)

    assert result is None


def test_handle_response_validation_error(monkeypatch):
    response = MagicMock()
    response.ok = False
    response.json.return_value = {
        "detail": [
            {"loc": ["body", "password"], "msg": "Too short"}
        ]
    }

    result = handle_response(response)

    assert result is None
