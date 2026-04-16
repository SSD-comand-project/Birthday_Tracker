import streamlit as st

from auth import auth_page
from views.birthdays import birthdays_today, birthdays_upcoming
from views.search import search_page
from views.profile import profile_page


def main():
    st.set_page_config(page_title="Birthday Tracker", layout="centered")

    st.sidebar.title("🎂 Birthday Tracker")

    st.markdown("""
    <style>
    .card {
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.5);
        transition: all 0.2s ease;
    }

    .card:hover {
        transform: scale(1.02);
        border: 1px solid #888;
    }
    </style>
    """, unsafe_allow_html=True)

    # Если не залогинен
    if "token" not in st.session_state:
        auth_page()
        return

    # Меню
    page = st.sidebar.selectbox(
        "Navigation",
        [
            "Today",
            "Upcoming",
            "Search",
            "Profile",
            "Logout",
        ],
    )

    if page == "Today":
        birthdays_today()

    elif page == "Upcoming":
        birthdays_upcoming()

    elif page == "Search":
        search_page()

    elif page == "Profile":
        profile_page()

    elif page == "Logout":
        st.session_state.clear()
        st.rerun()


if __name__ == "__main__":
    main()