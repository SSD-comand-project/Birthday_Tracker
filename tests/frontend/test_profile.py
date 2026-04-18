from app.frontend.views.profile import profile_page
from unittest.mock import patch


@patch("app.frontend.views.profile.requests.get")
def test_profile_load(mock_get):
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = {
        "full_name": "John",
        "birth_date": "2000-01-01"
    }

    profile_page()
