from app.frontend.views.search import search_page
from unittest.mock import patch
import streamlit as st


@patch("app.frontend.views.search.requests.get")
def test_search_results(mock_get, monkeypatch):
    monkeypatch.setattr(st, "button", lambda x: True)
    monkeypatch.setattr(st, "text_input", lambda x: "John")

    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = [
        {"full_name": "John Doe", "birth_date": "2000-01-01"}
    ]

    search_page()
