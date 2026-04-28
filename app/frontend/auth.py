import streamlit as st
import requests
from app.frontend.api import API_URL, REQUEST_TIMEOUT, handle_response
from datetime import date


def login(username, password):
    response = requests.post(
        f"{API_URL}/login",
        json={"username": username, "password": password},
        timeout=REQUEST_TIMEOUT,
    )

    data = handle_response(response)
    if data is None:
        return

    st.session_state["token"] = data["access_token"]
    st.success("Logged in!")
    st.rerun()


def register(username, password, full_name, birth_date):
    response = requests.post(
        f"{API_URL}/register",
        json={
            "username": username,
            "password": password,
            "full_name": full_name,
            "birth_date": birth_date,
        },
        timeout=REQUEST_TIMEOUT,
    )

    data = handle_response(response)
    if data is None:
        return

    st.session_state["token"] = data["access_token"]
    st.success("Registered successfully!")
    st.rerun()


def auth_page():
    st.title("🔐 Authentication")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            login(username, password)

    with tab2:
        username = st.text_input("Username", key="reg_user")
        password = st.text_input("Password", type="password", key="reg_pass")
        full_name = st.text_input("Full Name")

        today = date.today()
        min_date = today.replace(year=today.year - 100)
        max_date = today

        birth_date = st.date_input(
            "Birth Date",
            value=today,
            min_value=min_date,
            max_value=max_date
        )

        if st.button("Register"):
            register(
                username,
                password,
                full_name,
                birth_date.isoformat(),
            )
