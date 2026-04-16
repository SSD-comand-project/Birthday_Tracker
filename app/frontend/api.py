import streamlit as st

API_URL = "http://localhost:8000"
REQUEST_TIMEOUT = 5


def get_headers():
    token = st.session_state.get("token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


def handle_response(response):
    # ❌ ошибка логина (не очищаем сессию!)
    if response.status_code == 401:
        try:
            data = response.json()
            st.error(data.get("detail", "Unauthorized"))
        except Exception:
            st.error("Unauthorized")
        return None

    # ❌ другие ошибки
    if not response.ok:
        try:
            data = response.json()

            if isinstance(data.get("detail"), list):
                for err in data["detail"]:
                    field = err.get("loc", [])[-1]
                    msg = err.get("msg", "Invalid input")
                    st.error(f"{field}: {msg}")
            else:
                st.error(data.get("detail", "Error"))

        except Exception:
            st.error("Unknown error")

        return None

    return response.json()
