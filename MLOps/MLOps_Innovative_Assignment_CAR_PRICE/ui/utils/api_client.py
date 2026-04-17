"""
API Client — Wrapper for all HTTP calls to FastAPI backend.
Automatically includes JWT token from Streamlit session state.
"""

import os
import requests
import streamlit as st

API_URL = os.environ.get("API_URL", "http://localhost:8000")


def _headers():
    """Build request headers with JWT if available."""
    headers = {"Content-Type": "application/json"}
    token = st.session_state.get("access_token")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def signup(username: str, email: str, password: str, role: str = "user") -> dict:
    """Register a new user."""
    try:
        resp = requests.post(
            f"{API_URL}/auth/signup",
            json={"username": username, "email": email, "password": password, "role": role},
            timeout=10
        )
        return resp.json() if resp.status_code in (200, 201) else {"error": resp.json().get("detail", "Signup failed")}
    except Exception as e:
        return {"error": str(e)}


def login(username: str, password: str) -> dict:
    """Authenticate and get JWT token."""
    try:
        resp = requests.post(
            f"{API_URL}/auth/login",
            json={"username": username, "password": password},
            timeout=10
        )
        if resp.status_code == 200:
            data = resp.json()
            st.session_state["access_token"] = data["access_token"]
            st.session_state["username"] = data["username"]
            st.session_state["role"] = data["role"]
            st.session_state["logged_in"] = True
            return data
        return {"error": resp.json().get("detail", "Login failed")}
    except Exception as e:
        return {"error": str(e)}


def get_profile() -> dict:
    """Get current user profile."""
    try:
        resp = requests.get(f"{API_URL}/auth/me", headers=_headers(), timeout=10)
        return resp.json() if resp.status_code == 200 else {"error": "Failed to get profile"}
    except Exception as e:
        return {"error": str(e)}


def predict(car_data: dict) -> dict:
    """Call prediction endpoint."""
    try:
        resp = requests.post(f"{API_URL}/predict", json=car_data, headers=_headers(), timeout=15)
        return resp.json() if resp.status_code == 200 else {"error": resp.json().get("detail", "Prediction failed")}
    except requests.exceptions.ConnectionError:
        return {"error": "API not available. Ensure the API server is running."}
    except Exception as e:
        return {"error": str(e)}


def get_predictions(page: int = 1, limit: int = 20) -> dict:
    """Get current user's prediction history."""
    try:
        resp = requests.get(
            f"{API_URL}/user/predictions",
            params={"page": page, "limit": limit},
            headers=_headers(),
            timeout=10
        )
        return resp.json() if resp.status_code == 200 else {"error": "Failed to get predictions"}
    except Exception as e:
        return {"error": str(e)}


def get_analytics() -> dict:
    """Get current user's analytics."""
    try:
        resp = requests.get(f"{API_URL}/user/analytics", headers=_headers(), timeout=10)
        return resp.json() if resp.status_code == 200 else {"error": "Failed to get analytics"}
    except Exception as e:
        return {"error": str(e)}


def get_admin_predictions(page: int = 1, limit: int = 50) -> dict:
    """Get all predictions (admin only)."""
    try:
        resp = requests.get(
            f"{API_URL}/admin/predictions",
            params={"page": page, "limit": limit},
            headers=_headers(),
            timeout=10
        )
        return resp.json() if resp.status_code == 200 else {"error": "Admin access required"}
    except Exception as e:
        return {"error": str(e)}


def get_admin_users() -> dict:
    """Get all users (admin only)."""
    try:
        resp = requests.get(f"{API_URL}/admin/users", headers=_headers(), timeout=10)
        return resp.json() if resp.status_code == 200 else {"error": "Admin access required"}
    except Exception as e:
        return {"error": str(e)}


def get_admin_metrics() -> dict:
    """Get system metrics (admin only)."""
    try:
        resp = requests.get(f"{API_URL}/admin/metrics", headers=_headers(), timeout=10)
        return resp.json() if resp.status_code == 200 else {"error": "Admin access required"}
    except Exception as e:
        return {"error": str(e)}


def get_health() -> dict:
    """Check API health."""
    try:
        resp = requests.get(f"{API_URL}/health", timeout=5)
        return resp.json() if resp.status_code == 200 else {"error": "API unhealthy"}
    except Exception as e:
        return {"error": str(e)}


def logout():
    """Clear session state."""
    for key in ["access_token", "username", "role", "logged_in"]:
        if key in st.session_state:
            del st.session_state[key]
