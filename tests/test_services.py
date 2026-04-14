from datetime import date, timedelta

from app.backend.services.users import (
    authenticate_user,
    delete_user,
    get_user_by_id,
    register_user,
    update_user_profile,
)
from app.backend.services.birthdays import get_birthdays_next_7_days, get_birthdays_today


def test_full_flow():
    # уникальные данные для теста
    username = f"test_user_{date.today().strftime('%H%M%S')}"
    password = "test1234"
    full_name = "Test User"

    # birthday = today
    birth_today = date.today().isoformat()

    # 1) register
    user_id = register_user(username, password, full_name, birth_today)
    assert isinstance(user_id, int) and user_id > 0

    # 2) login success
    user = authenticate_user(username, password)
    assert user is not None
    assert user["username"] == username

    # 3) login fail
    bad_user = authenticate_user(username, "wrong-password")
    assert bad_user is None

    # 4) birthdays today
    today_list = get_birthdays_today()
    assert any(u["username"] == username for u in today_list)

    # 5) update profile (change name + birth_date to +3 days)
    new_name = "Updated Test User"
    new_birth = (date.today() + timedelta(days=3)).isoformat()
    updated = update_user_profile(user_id, new_name, new_birth)
    assert updated is True

    updated_user = get_user_by_id(user_id)
    assert updated_user is not None
    assert updated_user["full_name"] == new_name
    assert updated_user["birth_date"] == new_birth

    # 6) birthdays next 7 days
    week_list = get_birthdays_next_7_days()
    assert any(u["id"] == user_id for u in week_list)

    # 7) delete account
    deleted = delete_user(user_id)
    assert deleted is True

    deleted_user = get_user_by_id(user_id)
    assert deleted_user is None
