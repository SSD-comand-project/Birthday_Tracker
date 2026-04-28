import pytest
from unittest.mock import MagicMock
import streamlit as st


@pytest.fixture(autouse=True)
def mock_streamlit(monkeypatch):
    """Мокаем Streamlit UI функции"""
    monkeypatch.setattr(st, "error", MagicMock())
    monkeypatch.setattr(st, "success", MagicMock())
    monkeypatch.setattr(st, "warning", MagicMock())
    monkeypatch.setattr(st, "info", MagicMock())
    monkeypatch.setattr(st, "rerun", MagicMock())
    monkeypatch.setattr(st, "markdown", MagicMock())
    monkeypatch.setattr(st, "header", MagicMock())
    monkeypatch.setattr(st, "text_input", MagicMock(return_value=""))
    monkeypatch.setattr(st, "button", MagicMock(return_value=False))
    monkeypatch.setattr(st, "date_input", MagicMock())
    monkeypatch.setattr(st, "session_state", {})
