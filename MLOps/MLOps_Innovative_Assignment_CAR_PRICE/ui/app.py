"""
Used Car Price Predictor — Enhanced Streamlit UI v2.0
Features:
  - Login / Signup with role selection
  - Role-based UI rendering (User / Admin)
  - Prediction form with API integration (User only)
  - Prediction history tab with pagination (User only)
  - User analytics with Plotly charts (User only)
  - Admin dashboard with system metrics, user management (Admin only)
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px

# Import utilities
import sys
sys.path.insert(0, os.path.dirname(__file__))
from utils.session import init_session, is_logged_in, is_admin, get_username, get_role
from utils.api_client import (
    signup, login, logout, predict, get_predictions,
    get_analytics, get_admin_predictions, get_admin_users,
    get_admin_metrics, get_health
)

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Used Car Price Predictor",
    page_icon="car",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Initialize Session ─────────────────────────────────────────────────────
init_session()

# ─── Custom CSS for Premium Look ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 { color: #e0e0ff !important; }

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 20px;
    }
    div[data-testid="stMetric"] label { color: #a5b4fc !important; }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #22d3ee !important; font-weight: 700 !important;
    }

    h1 { color: #e0e0ff !important; font-weight: 800 !important; }
    h2 { color: #c4b5fd !important; }
    h3 { color: #a5b4fc !important; }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px; background: rgba(255,255,255,0.03);
        border-radius: 12px; padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px; color: #a5b4fc; font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(99, 102, 241, 0.3) !important; color: white !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important; border: none !important; border-radius: 12px !important;
        padding: 12px 32px !important; font-weight: 600 !important; font-size: 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.6) !important;
    }

    div[data-baseweb="select"] > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 10px !important; color: white !important;
    }
    .stNumberInput > div > div > input, .stTextInput > div > div > input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 10px !important; color: white !important;
    }

    .price-card {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a78bfa 100%);
        border-radius: 20px; padding: 40px; text-align: center;
        box-shadow: 0 20px 40px rgba(99, 102, 241, 0.3); margin: 20px 0;
    }
    .price-card h2 { color: rgba(255,255,255,0.8) !important; font-size: 18px; margin-bottom: 10px; }
    .price-card .price { color: white; font-size: 48px; font-weight: 800; line-height: 1.2; }
    .price-card .subtitle { color: rgba(255,255,255,0.7); font-size: 14px; margin-top: 8px; }

    .glass-card {
        background: rgba(255,255,255,0.05); backdrop-filter: blur(16px);
        border: 1px solid rgba(255,255,255,0.1); border-radius: 20px;
        padding: 24px; margin: 12px 0;
    }

    .hero {
        background: linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(139,92,246,0.1) 100%);
        border: 1px solid rgba(99,102,241,0.2); border-radius: 24px;
        padding: 32px; margin-bottom: 24px;
    }

    .auth-card {
        background: rgba(255,255,255,0.05); backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.1); border-radius: 24px;
        padding: 40px; max-width: 450px; margin: 40px auto;
    }

    .student-card {
        background: linear-gradient(135deg, rgba(99,102,241,0.1) 0%, rgba(139,92,246,0.08) 100%);
        border: 1px solid rgba(99,102,241,0.15); border-radius: 16px;
        padding: 20px; margin: 8px 0; text-align: center;
    }
    .student-card .name { color: #e0e0ff; font-weight: 600; font-size: 15px; }
    .student-card .roll { color: #a5b4fc; font-size: 13px; }

    .stat-box {
        background: linear-gradient(135deg, rgba(99,102,241,0.2) 0%, rgba(139,92,246,0.15) 100%);
        border: 1px solid rgba(99,102,241,0.25); border-radius: 16px;
        padding: 24px; text-align: center;
    }
    .stat-box .stat-value { color: #22d3ee; font-size: 32px; font-weight: 800; }
    .stat-box .stat-label { color: #a5b4fc; font-size: 13px; margin-top: 4px; }

    hr { border-color: rgba(255,255,255,0.08) !important; }
</style>
""", unsafe_allow_html=True)


def format_price(price):
    """Format price in Indian Rupee style."""
    if price >= 100000:
        return f"Rs. {price/100000:.2f} Lakh"
    else:
        return f"Rs. {price:,.0f}"


# ══════════════════════════════════════════════════════════════════════════════
# AUTH PAGE — Login / Signup
# ══════════════════════════════════════════════════════════════════════════════
def render_auth_page():
    st.markdown("""
    <div class="hero" style="text-align: center;">
        <h1 style="margin:0; font-size: 36px;">Used Car Price Predictor</h1>
        <p style="color: rgba(255,255,255,0.6); font-size: 16px; margin-top: 8px;">
            AI-powered price estimation | MLOps Pipeline v2.0
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab_login, tab_signup = st.tabs(["Login", "Sign Up"])

        with tab_login:
            st.markdown("### Welcome Back!")
            username = st.text_input("Username", key="login_username", placeholder="Enter username")
            password = st.text_input("Password", type="password", key="login_password", placeholder="Enter password")

            if st.button("Login", key="login_btn", use_container_width=True):
                if username and password:
                    with st.spinner("Authenticating..."):
                        result = login(username, password)
                    if "error" in result:
                        st.error(f"Login failed: {result['error']}")
                    else:
                        st.success(f"Welcome back, {result['username']}! (Role: {result['role']})")
                        st.rerun()
                else:
                    st.warning("Please enter both username and password.")

        with tab_signup:
            st.markdown("### Create Account")
            new_username = st.text_input("Username", key="signup_username", placeholder="Choose a username")
            new_email = st.text_input("Email", key="signup_email", placeholder="your@email.com")
            new_password = st.text_input("Password", type="password", key="signup_password", placeholder="Min 6 characters")
            new_role = st.selectbox("Role", ["user", "admin"], key="signup_role")

            if st.button("Create Account", key="signup_btn", use_container_width=True):
                if new_username and new_email and new_password:
                    with st.spinner("Creating account..."):
                        result = signup(new_username, new_email, new_password, new_role)
                    if "error" in result:
                        st.error(f"{result['error']}")
                    else:
                        st.success("Account created! Logging you in...")
                        login_result = login(new_username, new_password)
                        if "error" not in login_result:
                            st.rerun()
                        else:
                            st.info("Account created. Please switch to the Login tab.")
                else:
                    st.warning("Please fill in all fields.")

    # API Health indicator
    health = get_health()
    if "error" not in health:
        st.markdown("""
        <div style="text-align: center; margin-top: 30px; color: rgba(255,255,255,0.3);">
            API Connected | Model: loaded | v2.0.0
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; margin-top: 30px; color: rgba(255,100,100,0.5);">
            API Not Connected — Start the API server first
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — Car Input Form (shown only for User role)
# ══════════════════════════════════════════════════════════════════════════════
def render_user_sidebar():
    with st.sidebar:
        st.markdown(f"### {get_username()}")
        st.markdown(f"**Role:** `{get_role()}`")

        if st.button("Logout", use_container_width=True):
            logout()
            st.rerun()

        st.markdown("---")
        st.markdown("## Car Details")
        st.markdown("---")

        car_name = st.text_input("Car Name", value="Maruti Swift Dzire VDI",
                                  help="Full car name including variant")

        col1, col2 = st.columns(2)
        with col1:
            year = st.number_input("Year", min_value=1990, max_value=2025, value=2018)
        with col2:
            seats = st.number_input("Seats", min_value=2, max_value=14, value=5)

        km_driven = st.slider("Kilometers Driven", min_value=0, max_value=500000,
                               value=45000, step=1000, format="%d km")

        col3, col4 = st.columns(2)
        with col3:
            fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
        with col4:
            transmission = st.selectbox("Transmission", ["Manual", "Automatic"])

        owner = st.selectbox("Owner Type",
                             ["First Owner", "Second Owner", "Third Owner",
                              "Fourth & Above Owner", "Test Drive Car"])

        seller_type = st.selectbox("Seller Type",
                                   ["Individual", "Dealer", "Trustmark Dealer"])

        st.markdown("---")
        st.markdown("### Specifications")

        mileage = st.number_input("Mileage (kmpl)", min_value=0.0, max_value=100.0,
                                   value=23.4, step=0.5)
        engine = st.number_input("Engine (CC)", min_value=500.0, max_value=6000.0,
                                  value=1248.0, step=50.0)
        max_power = st.number_input("Max Power (bhp)", min_value=20.0, max_value=600.0,
                                     value=74.0, step=5.0)

        st.markdown("---")
        predict_btn = st.button("Predict Price", use_container_width=True)

    return {
        "name": car_name, "year": year, "km_driven": km_driven,
        "fuel": fuel, "transmission": transmission, "owner": owner,
        "seller_type": seller_type, "mileage": mileage, "engine": engine,
        "max_power": max_power, "seats": seats,
    }, predict_btn


def render_admin_sidebar():
    """Admin sidebar — no car input, just profile and navigation."""
    with st.sidebar:
        st.markdown(f"### {get_username()}")
        st.markdown(f"**Role:** `{get_role()}`")

        if st.button("Logout", use_container_width=True):
            logout()
            st.rerun()

        st.markdown("---")
        st.markdown("## Admin Panel")
        st.markdown("""
        <div class="glass-card" style="padding: 16px;">
            <p style="color: #a5b4fc; font-size: 13px; margin: 0;">
                Manage users, view system metrics, and monitor the MLOps pipeline.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Quick Links")
        st.markdown("""
        <div style="line-height: 2.4;">
            <a href="http://localhost:3000/d/car-price-admin-dashboard" target="_blank" style="color: #22d3ee; text-decoration: none;">Grafana Admin Dashboard</a><br>
            <a href="http://localhost:3000/d/car-price-user-dashboard" target="_blank" style="color: #22d3ee; text-decoration: none;">Grafana User Dashboard</a><br>
            <a href="http://localhost:9090/targets" target="_blank" style="color: #22d3ee; text-decoration: none;">Prometheus Targets</a><br>
            <a href="http://localhost:5000" target="_blank" style="color: #22d3ee; text-decoration: none;">MLflow Experiments</a><br>
            <a href="http://localhost:8000/docs" target="_blank" style="color: #22d3ee; text-decoration: none;">API Documentation</a>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PREDICTION TAB (User only)
# ══════════════════════════════════════════════════════════════════════════════
def render_prediction_tab(car_data, predict_btn):
    if predict_btn:
        with st.spinner("Analyzing car value..."):
            result = predict(car_data)

        if "error" in result:
            st.error(f"Prediction failed: {result['error']}")
        else:
            price = result["predicted_price"]

            st.markdown(f"""
            <div class="price-card">
                <h2>Estimated Market Value</h2>
                <div class="price">{format_price(price)}</div>
                <div class="subtitle">Based on {car_data['name']} | {car_data['year']} | {car_data['km_driven']:,} km</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("### Prediction Summary")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Predicted Price", format_price(price))
            col2.metric("Car Age", f"{2025 - car_data['year']} years")
            col3.metric("Km Driven", f"{car_data['km_driven']:,}")
            col4.metric("Fuel", car_data['fuel'])

            # Confidence Range
            low, high = price * 0.85, price * 1.15
            st.markdown("### Price Range Estimate")
            st.markdown(f"""
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="color: #a5b4fc; font-size: 14px;">Low Estimate</span><br>
                        <span style="color: #22d3ee; font-size: 22px; font-weight: 700;">{format_price(low)}</span>
                    </div>
                    <div style="text-align: center;">
                        <span style="color: #a5b4fc; font-size: 14px;">Best Estimate</span><br>
                        <span style="color: #10b981; font-size: 28px; font-weight: 800;">{format_price(price)}</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="color: #a5b4fc; font-size: 14px;">High Estimate</span><br>
                        <span style="color: #f472b6; font-size: 22px; font-weight: 700;">{format_price(high)}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 60px;">
            <h2 style="color: #a5b4fc !important;">Enter Car Details</h2>
            <p style="color: rgba(255,255,255,0.5);">
                Fill in the car specifications in the sidebar and click <strong>Predict Price</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HISTORY TAB (User only)
# ══════════════════════════════════════════════════════════════════════════════
def render_history_tab():
    st.markdown("### Your Prediction History")
    data = get_predictions(page=1, limit=50)

    if "error" in data:
        st.warning(f"{data['error']}")
        return

    predictions = data.get("predictions", [])
    if not predictions:
        st.info("No predictions yet. Make your first prediction!")
        return

    st.markdown(f"**Total predictions:** {data.get('total', 0)}")

    rows = []
    for p in predictions:
        inp = p.get("input", {})
        pred = p.get("prediction", {})
        rows.append({
            "Car": inp.get("name", "N/A"),
            "Year": inp.get("year", ""),
            "Predicted Price": format_price(pred.get("predicted_price", 0)),
            "Fuel": inp.get("fuel", ""),
            "Transmission": inp.get("transmission", ""),
            "Km Driven": f"{inp.get('km_driven', 0):,}",
            "Response (ms)": p.get("response_time_ms", ""),
            "Date": str(p.get("timestamp", ""))[:19],
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    if len(predictions) >= 2:
        st.markdown("### Your Prediction Trends")
        trend_data = []
        for p in predictions:
            trend_data.append({
                "timestamp": p.get("timestamp", ""),
                "price": p.get("prediction", {}).get("predicted_price", 0)
            })
        trend_df = pd.DataFrame(trend_data)

        fig = px.line(trend_df, x="timestamp", y="price",
                      title="Predicted Prices Over Time",
                      labels={"price": "Price (INR)", "timestamp": "Time"},
                      markers=True)
        fig.update_traces(line_color="#8b5cf6", marker_color="#22d3ee")
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e0e0ff", family="Inter"),
            margin=dict(l=0, r=0, t=40, b=0), height=400,
        )
        st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# ANALYTICS TAB (User only)
# ══════════════════════════════════════════════════════════════════════════════
def render_analytics_tab():
    st.markdown("### Your Analytics")
    data = get_analytics()

    if "error" in data:
        st.warning(f"{data['error']}")
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Predictions", data.get("total_predictions", 0))
    col2.metric("Avg Predicted Price", format_price(data.get("avg_predicted_price", 0)))
    col3.metric("Unique Brands", len(data.get("most_predicted_brands", [])))

    brands = data.get("most_predicted_brands", [])
    if brands:
        st.markdown("### Most Predicted Brands")
        brand_df = pd.DataFrame(brands)
        fig = px.bar(brand_df, x="brand", y="count",
                     color="count", color_continuous_scale=["#6366f1", "#a78bfa"],
                     title="Top Brands by Prediction Count")
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e0e0ff", family="Inter"),
            showlegend=False, coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=40, b=0), height=350,
        )
        st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# ADMIN — System Metrics Tab
# ══════════════════════════════════════════════════════════════════════════════
def render_admin_metrics_tab():
    st.markdown("### System Metrics")

    metrics = get_admin_metrics()
    if "error" not in metrics:
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Users", metrics.get("total_users", 0))
        col2.metric("Total Predictions", metrics.get("total_predictions", 0))
        col3.metric("Avg Response (ms)", f"{metrics.get('avg_response_time_ms', 0):.1f}")
        col4.metric("Today's Predictions", metrics.get("predictions_today", 0))
        col5.metric("Active Users (24h)", metrics.get("active_users", 0))
    else:
        st.warning("Unable to load system metrics.")

    st.markdown("---")

    # Grafana Dashboard Links
    st.markdown("### Grafana Dashboards")
    st.markdown("""
    <div class="glass-card">
        <p style="color: #a5b4fc;">Access detailed monitoring dashboards:</p>
        <ul style="color: rgba(255,255,255,0.7); line-height: 2.2; list-style: none; padding: 0;">
            <li>-- <a href="http://localhost:3000/d/car-price-admin-dashboard" target="_blank" style="color: #22d3ee;">Admin Dashboard (Grafana)</a></li>
            <li>-- <a href="http://localhost:3000/d/car-price-user-dashboard" target="_blank" style="color: #22d3ee;">User Dashboard (Grafana)</a></li>
            <li>-- <a href="http://localhost:9090/targets" target="_blank" style="color: #22d3ee;">Prometheus Targets</a></li>
            <li>-- <a href="http://localhost:5000" target="_blank" style="color: #22d3ee;">MLflow Experiments</a></li>
            <li>-- <a href="http://localhost:8000/docs" target="_blank" style="color: #22d3ee;">API Documentation (Swagger)</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ADMIN — User Management Tab
# ══════════════════════════════════════════════════════════════════════════════
def render_admin_users_tab():
    st.markdown("### Registered Users")
    users = get_admin_users()
    if isinstance(users, list) and users:
        user_rows = []
        for u in users:
            user_rows.append({
                "Username": u.get("username", ""),
                "Email": u.get("email", ""),
                "Role": u.get("role", ""),
                "Active": "Yes" if u.get("is_active", True) else "No",
                "Created": str(u.get("created_at", ""))[:19],
            })
        st.dataframe(pd.DataFrame(user_rows), use_container_width=True, hide_index=True)

        # User stats
        st.markdown("### User Statistics")
        user_df = pd.DataFrame(user_rows)
        col1, col2 = st.columns(2)
        with col1:
            role_counts = user_df["Role"].value_counts()
            fig = px.pie(values=role_counts.values, names=role_counts.index,
                         title="Users by Role",
                         color_discrete_sequence=["#6366f1", "#22d3ee"])
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e0e0ff", family="Inter"),
                margin=dict(l=0, r=0, t=40, b=0), height=300,
            )
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-value">{len(users)}</div>
                <div class="stat-label">Total Registered Users</div>
            </div>
            """, unsafe_allow_html=True)
            admins = sum(1 for u in users if u.get("role") == "admin")
            regular = len(users) - admins
            st.markdown(f"""
            <div style="display: flex; gap: 12px; margin-top: 12px;">
                <div class="stat-box" style="flex: 1;">
                    <div class="stat-value" style="font-size: 24px;">{admins}</div>
                    <div class="stat-label">Admins</div>
                </div>
                <div class="stat-box" style="flex: 1;">
                    <div class="stat-value" style="font-size: 24px;">{regular}</div>
                    <div class="stat-label">Users</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No users registered yet.")


# ══════════════════════════════════════════════════════════════════════════════
# ADMIN — All Predictions Tab
# ══════════════════════════════════════════════════════════════════════════════
def render_admin_predictions_tab():
    st.markdown("### All Predictions (System-wide)")
    all_preds = get_admin_predictions(page=1, limit=50)
    if "error" not in all_preds:
        preds = all_preds.get("predictions", [])
        if preds:
            rows = []
            for p in preds:
                inp = p.get("input", {})
                pred = p.get("prediction", {})
                rows.append({
                    "User": p.get("user_id", "")[:8] + "...",
                    "Car": inp.get("name", "N/A"),
                    "Year": inp.get("year", ""),
                    "Price": format_price(pred.get("predicted_price", 0)),
                    "Fuel": inp.get("fuel", ""),
                    "Model Version": pred.get("model_version", "N/A"),
                    "Response (ms)": p.get("response_time_ms", ""),
                    "Date": str(p.get("timestamp", ""))[:19],
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
            st.caption(f"Showing {len(preds)} of {all_preds.get('total', 0)} total predictions")

            # Price distribution chart
            if len(preds) >= 2:
                st.markdown("### Price Distribution")
                prices = [p.get("prediction", {}).get("predicted_price", 0) for p in preds]
                fig = px.histogram(x=prices, nbins=20, title="Predicted Price Distribution",
                                   labels={"x": "Price (INR)", "y": "Count"},
                                   color_discrete_sequence=["#8b5cf6"])
                fig.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#e0e0ff", family="Inter"),
                    margin=dict(l=0, r=0, t=40, b=0), height=350,
                    showlegend=False,
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No predictions in the system yet.")
    else:
        st.warning("Unable to load predictions.")


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER WITH STUDENT NAMES
# ══════════════════════════════════════════════════════════════════════════════
def render_footer():
    st.markdown("---")

    # Student names and submission details
    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        <h3 style="color: #c4b5fd !important; margin-bottom: 4px;">MLOps Project Submission</h3>
        <p style="color: rgba(255,255,255,0.4); font-size: 13px; margin-bottom: 16px;">
            M.Tech Semester 2 | Nirma University | Subject Guide: Dr. Priyank Thakkar Sir
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    students = [
        ("Vraj Prajapati", "25MCE020"),
        ("Dev Patel", "25MCD015"),
        ("Kinjal Rathod", "25MCD009"),
        ("Soham Dave", "25MCD005"),
    ]
    for col, (name, roll) in zip([col1, col2, col3, col4], students):
        with col:
            st.markdown(f"""
            <div class="student-card">
                <div class="name">{name}</div>
                <div class="roll">{roll}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; color: rgba(255,255,255,0.25); padding: 16px 0 8px;">
        <p style="font-size: 12px;">Built with MLOps Best Practices |
        <strong>FastAPI</strong> | <strong>MongoDB</strong> |
        <strong>MLflow</strong> | <strong>Prometheus</strong> | <strong>Grafana</strong> |
        <strong>Docker</strong> | <strong>Jenkins</strong></p>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN APP LOGIC
# ══════════════════════════════════════════════════════════════════════════════

if not is_logged_in():
    render_auth_page()
    render_footer()
else:
    if is_admin():
        # ── ADMIN VIEW ──────────────────────────────────────────────────
        render_admin_sidebar()

        st.markdown(f"""
        <div class="hero">
            <h1 style="margin:0; font-size: 36px;">Admin Dashboard</h1>
            <p style="color: rgba(255,255,255,0.6); font-size: 16px; margin-top: 8px;">
                MLOps Pipeline v2.0 | Logged in as <strong>{get_username()}</strong> (admin)
            </p>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs([
            "System Metrics", "User Management", "All Predictions"
        ])
        with tab1:
            render_admin_metrics_tab()
        with tab2:
            render_admin_users_tab()
        with tab3:
            render_admin_predictions_tab()

        render_footer()

    else:
        # ── USER VIEW ───────────────────────────────────────────────────
        car_data, predict_btn = render_user_sidebar()

        st.markdown(f"""
        <div class="hero">
            <h1 style="margin:0; font-size: 36px;">Used Car Price Predictor</h1>
            <p style="color: rgba(255,255,255,0.6); font-size: 16px; margin-top: 8px;">
                AI-powered price estimation | MLOps Pipeline v2.0 | Logged in as <strong>{get_username()}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs([
            "Price Prediction", "Prediction History", "Analytics"
        ])
        with tab1:
            render_prediction_tab(car_data, predict_btn)
        with tab2:
            render_history_tab()
        with tab3:
            render_analytics_tab()

        render_footer()
