import streamlit as st
import requests
from api import API_URL, REQUEST_TIMEOUT, get_headers, handle_response


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


def search_page():
    st.header("🔍 Search Users")

    query = st.text_input("Enter full name")

    if st.button("Search"):
        response = requests.get(
            f"{API_URL}/birthdays/search",
            params={"name": query},
            headers=get_headers(),
            timeout=REQUEST_TIMEOUT,
        )

        data = handle_response(response)
        if data is None:
            return

        if not data:
            st.info("No users found")
            return

        for user in data:
            render_user_card(user)
