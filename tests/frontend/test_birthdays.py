from app.frontend.views.birthdays import birthdays_today
from unittest.mock import patch


@patch("app.frontend.views.birthdays.requests.get")
def test_birthdays_today_success(mock_get):
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = [
        {"full_name": "John", "birth_date": "2000-01-01"}
    ]

    birthdays_today()  # не должен упасть


@patch("app.frontend.views.birthdays.requests.get")
def test_birthdays_today_empty(mock_get):
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = []

    birthdays_today()
