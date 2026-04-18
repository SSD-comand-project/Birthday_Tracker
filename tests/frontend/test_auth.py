from app.frontend.auth import login, register
from unittest.mock import patch
import streamlit as st


@patch("app.frontend.auth.requests.post")
def test_login_success(mock_post):
    mock_post.return_value.ok = True
    mock_post.return_value.json.return_value = {
        "access_token": "token123"
    }

    login("user", "password")

    assert st.session_state["token"] == "token123"


@patch("app.frontend.auth.requests.post")
def test_login_fail(mock_post):
    mock_post.return_value.status_code = 401
    mock_post.return_value.ok = False
    mock_post.return_value.json.return_value = {
        "detail": "Incorrect username or password"
    }

    login("user", "wrong")

    assert "token" not in st.session_state


@patch("app.frontend.auth.requests.post")
def test_register_success(mock_post):
    mock_post.return_value.ok = True
    mock_post.return_value.json.return_value = {
        "access_token": "token123"
    }

    register("user", "password123", "Name", "2000-01-01")

    assert st.session_state["token"] == "token123"
