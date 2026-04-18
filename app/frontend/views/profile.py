import streamlit as st
import requests
from datetime import date
from app.frontend.api import (
    API_URL,
    REQUEST_TIMEOUT,
    get_headers,
    handle_response,
)


def profile_page():
    st.header("👤 My Profile")

    response = requests.get(
        f"{API_URL}/users/me",
        headers=get_headers(),
        timeout=REQUEST_TIMEOUT,
    )

    user = handle_response(response)
    if user is None:
        return

    full_name = st.text_input("Full Name", value=user["full_name"])
    birth_date = st.date_input(
        "Birth Date",
        value=date.fromisoformat(user["birth_date"]),
    )

    if st.button("Update profile"):
        response = requests.put(
            f"{API_URL}/users/me",
            json={
                "full_name": full_name,
                "birth_date": birth_date.isoformat(),
            },
            headers=get_headers(),
            timeout=REQUEST_TIMEOUT,
        )

        data = handle_response(response)
        if data:
            st.success("Profile updated")

    if st.button("Delete account"):
        response = requests.delete(
            f"{API_URL}/users/me",
            headers=get_headers(),
            timeout=REQUEST_TIMEOUT,
        )

        if response.status_code == 204:
            st.session_state.clear()
            st.success("Account deleted")
            st.rerun()
