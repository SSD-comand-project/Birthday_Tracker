import streamlit as st
import requests
from app.frontend.api import (
    API_URL,
    REQUEST_TIMEOUT,
    get_headers,
    handle_response,
)


def render_user_card(user):
    st.markdown(
        f"""
        <div class="card">
            <div style="font-size: 18px; font-weight: 600;">
                👤 {user['full_name']}
            </div>
            <div style="opacity: 0.7; margin-top: 4px;">
                🗓️ {user['birth_date']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def birthdays_today():
    st.header("🎉 Today's Birthdays")

    response = requests.get(
        f"{API_URL}/birthdays/today",
        headers=get_headers(),
        timeout=REQUEST_TIMEOUT,
    )

    data = handle_response(response)
    if data is None:
        return

    if not data:
        st.info("No birthdays today")
        return

    for user in data:
        render_user_card(user)


def birthdays_upcoming():
    st.header("🗓️ Upcoming Birthdays (7 days)")

    response = requests.get(
        f"{API_URL}/birthdays/upcoming",
        headers=get_headers(),
        timeout=REQUEST_TIMEOUT,
    )

    data = handle_response(response)
    if data is None:
        return

    if not data:
        st.info("No upcoming birthdays")
        return

    for user in data:
        render_user_card(user)
