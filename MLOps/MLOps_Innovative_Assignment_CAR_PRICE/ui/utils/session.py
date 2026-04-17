"""
Session State Management for Streamlit.
Initializes and manages session state keys.
"""

import streamlit as st


def init_session():
    """Initialize session state with defaults."""
    defaults = {
        "access_token": None,
        "username": None,
        "role": None,
        "logged_in": False,
        "current_page": "auth",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def is_logged_in() -> bool:
    """Check if user is logged in."""
    return st.session_state.get("logged_in", False)


def is_admin() -> bool:
    """Check if current user is admin."""
    return st.session_state.get("role") == "admin"


def get_username() -> str:
    """Get current username."""
    return st.session_state.get("username", "")


def get_role() -> str:
    """Get current user role."""
    return st.session_state.get("role", "")
