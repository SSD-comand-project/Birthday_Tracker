import streamlit as st
import requests
from api import API_URL
from api import handle_response



def login(username, password):
    response = requests.post(
        f"{API_URL}/login",
        json={"username": username, "password": password},
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
        birth_date = st.date_input("Birth Date")

        if st.button("Register"):
            register(
                username,
                password,
                full_name,
                birth_date.isoformat(),
            )