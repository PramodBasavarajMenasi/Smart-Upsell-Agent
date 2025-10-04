# smart_upsell_dashboard.py
"""
Smart Upsell Agent - Streamlit Frontend with Sidebar, Main Title, and dotenv integration
"""

import os
import time
import datetime
from typing import Optional

import streamlit as st
import pandas as pd
import psycopg2
import requests
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# -------------------------
# Load environment variables
# -------------------------
load_dotenv()

# Streamlit page config
st.set_page_config(page_title="Smart Upsell Agent Dashboard", layout="wide")

# -------------------------
# Main Page Title
# -------------------------
st.title("🚀 Smart Upsell Agent Dashboard")
st.caption("An AI-powered system to identify upsell opportunities and trigger personalized campaigns.")

# -------------------------
# Configuration (from .env)
# -------------------------
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

CAMPAIGN_TRIGGER_WEBHOOK = os.getenv(
    "CAMPAIGN_TRIGGER_WEBHOOK"
)
USER_ACTIVITY_WEBHOOK = os.getenv(
    "USER_ACTIVITY_WEBHOOK"
)

# -------------------------
# Demo Data
# -------------------------
_demo_user_activities = pd.DataFrame([
    {"id": 1, "user_id": "sarah_designer", "feature_used": "export_report", "email": "sarah@example.com",
     "timestamp": datetime.datetime.utcnow()},
    {"id": 2, "user_id": "john_agency", "feature_used": "file_share", "email": "john@example.com",
     "timestamp": datetime.datetime.utcnow()},
])
_demo_upsell_ops = pd.DataFrame([
    {"id": 1, "user_id": "sarah_designer", "ai_score": 92, "email": "sarah@example.com",
     "recommended_feature": "Pro Exports", "reasoning": "Frequent exports", "created_at": datetime.datetime.utcnow(),
     "status": "active"},
    {"id": 2, "user_id": "john_agency", "ai_score": 65, "email": "john@example.com", "recommended_feature": "Team Plan",
     "reasoning": "Multiple teammates", "created_at": datetime.datetime.utcnow() - datetime.timedelta(hours=2),
     "status": "active"},
])
_demo_campaigns = pd.DataFrame([
    {"id": 1, "opportunity_id": 1, "user_id": "sarah_designer", "recommended_feature": "Pro Exports",
     "subject_line": "Try Pro Exports", "email_message": "Upgrade to pro to export...", "email_to": "sarah@example.com",
     "campaign_type": "email", "ai_score": 92, "sent_at": datetime.datetime.utcnow(), "delivery_status": "sent",
     "open_count": 1, "click_count": 1, "created_at": datetime.datetime.utcnow()},
])

# -------------------------
# DB Helpers
# -------------------------
@st.cache_resource
def init_db_conn():
    try:
        if not DB_CONFIG["host"] or not DB_CONFIG["password"]:
            return None
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            dbname=DB_CONFIG["dbname"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            connect_timeout=5
        )
        return conn
    except Exception:
        return None

def safe_read_sql(query: str, conn) -> pd.DataFrame:
    try:
        if conn is None:
            return pd.DataFrame()
        return pd.read_sql(query, conn)
    except Exception:
        return pd.DataFrame()

def safe_execute(query: str, params: tuple, conn) -> bool:
    try:
        if conn is None:
            return False
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        cur.close()
        return True
    except Exception:
        return False

# -------------------------
# Main Application
# -------------------------
conn = init_db_conn()
db_available = conn is not None

# KPI panel
def get_aggregates():
    if db_available:
        try:
            users_today = int(safe_read_sql(
                "SELECT COUNT(DISTINCT user_id) FROM user_activities WHERE timestamp >= CURRENT_DATE;", conn
            ).iat[0, 0])
        except:
            users_today = 0
        try:
            emails_sent = int(safe_read_sql("SELECT COUNT(*) FROM campaign_history;", conn).iat[0, 0])
        except:
            emails_sent = 0
        try:
            conversions = int(safe_read_sql(
                "SELECT COUNT(*) FROM campaign_history WHERE COALESCE(open_count,0) > 0 OR COALESCE(click_count,0) > 0;", conn
            ).iat[0, 0])
        except:
            conversions = 0
    else:
        users_today = _demo_user_activities["user_id"].nunique()
        emails_sent = len(_demo_campaigns)
        conversions = _demo_campaigns[(_demo_campaigns["click_count"] > 0)].shape[0]

    success_rate = round((conversions / emails_sent) * 100, 2) if emails_sent > 0 else 0
    return users_today, emails_sent, conversions, success_rate

users_today, emails_sent, conversions, success_rate = get_aggregates()


st.sidebar.subheader("ℹ️ Project Overview")
st.sidebar.write(
    """
    This AI-powered dashboard identifies upsell opportunities, tracks user activity, and automates campaigns.  
    It demonstrates how AI insights improve conversion rates by detecting upgrade opportunities and triggering campaigns in real-time.
    """
)

# -------------------------
# Main KPIs in columns
# -------------------------
k1, k2, k3, k4 = st.columns(4)
k1.metric("👥 Active Users Today", users_today)
k2.metric("📩 Emails Sent", emails_sent)
k3.metric("✅ Conversions", conversions)
k4.metric("📈 Conversion Rate", f"{success_rate}%")

# Agent uplift
BASELINE_RATE = 2.0
uplift = round(success_rate - BASELINE_RATE, 2)
pct_uplift = round((success_rate / BASELINE_RATE - 1) * 100, 2) if BASELINE_RATE > 0 else None
st.markdown(
    f"**Agent Impact:** baseline {BASELINE_RATE}% → live {success_rate}% (uplift: {uplift} pts, ~{pct_uplift}% relative)"
)
st.markdown("---")

# -------------------------
# Tabs (Activities, Opportunities, Campaigns, Analytics)
# -------------------------
tab_activities, tab_ops, tab_campaigns, tab_analytics = st.tabs(
    ["User Activities", "AI Opportunities", "Campaigns", "Analytics & Impact"]
)

# Remaining tabs code (same as your current implementation)


# TAB: Activities
with tab_activities:
    st.header("📝 Track User Activity")
    with st.form("activity_form", clear_on_submit=True):
        user_id = st.text_input("User ID", "sarah_designer")
        feature_used = st.selectbox("Feature Used",
                                    ["export_report", "file_share", "integration_setup", "dashboard_view"])
        email = st.text_input("Email", f"{user_id}@example.com")
        plan_type = st.selectbox("Plan Type", ["free", "pro", "enterprise"])
        session_id = st.text_input("Session ID", f"session_{int(time.time())}")
        submit = st.form_submit_button("📥 Track Activity")

    if submit:
        payload = {"user_id": user_id, "feature": feature_used, "email": email, "plan_type": plan_type,
                   "session_id": session_id, "timestamp": datetime.datetime.utcnow().isoformat()}
        try:
            r = requests.post(USER_ACTIVITY_WEBHOOK, json=payload, timeout=8)
            if 200 <= r.status_code < 300:
                st.success("✅ Activity sent successfully to n8n webhook.")
                try:
                    st.json(r.json())
                except:
                    st.write("Webhook responded (non-JSON).")
            else:
                st.error(f"❌ Webhook returned {r.status_code}: {r.text}")
        except Exception as e:
            st.error(f"⚠️ Failed to call webhook: {e}")
            st.json(payload)

    st.markdown("### Recent Activities")
    if db_available:
        df_act = safe_read_sql(
            "SELECT id, user_id, feature_used, email, timestamp FROM user_activities ORDER BY timestamp DESC LIMIT 20;", conn)
        st.dataframe(df_act if not df_act.empty else _demo_user_activities)
    else:
        st.dataframe(_demo_user_activities)

# TAB: Opportunities
with tab_ops:
    st.header("🤖 AI Upsell Opportunities")
    if db_available:
        df_ops = safe_read_sql(
            "SELECT id, user_id, email, recommended_feature, ai_score, reasoning, created_at, status FROM upsell_opportunities ORDER BY created_at DESC LIMIT 50;", conn)
        if df_ops.empty: df_ops = _demo_upsell_ops
    else:
        df_ops = _demo_upsell_ops
        st.warning("DB not connected — showing demo data.")

    st.dataframe(df_ops)

    st.markdown("### Trigger Campaign for Opportunity")
    opp_for_campaign = st.number_input("Opportunity ID", min_value=0, value=0, step=1)
    if st.button("📤 Trigger Campaign"):
        if opp_for_campaign > 0:
            payload = {"opportunity_id": int(opp_for_campaign)}
            try:
                r = requests.post(CAMPAIGN_TRIGGER_WEBHOOK, json=payload, timeout=10)
                if 200 <= r.status_code < 300:
                    st.success("Campaign trigger sent.")
                    try:
                        st.json(r.json())
                    except:
                        st.write("Webhook responded (non-json).")
                else:
                    st.error(f"Webhook error {r.status_code}: {r.text}")
            except Exception as e:
                st.error(f"Failed to call campaign webhook: {e}")
        else:
            st.warning("Enter valid opportunity id > 0.")

# TAB: Campaigns
with tab_campaigns:
    st.header("📬 Campaign History")
    if db_available:
        df_c = safe_read_sql("SELECT * FROM campaign_history ORDER BY sent_at DESC LIMIT 50;", conn)
        if df_c.empty: df_c = _demo_campaigns
    else:
        df_c = _demo_campaigns
        st.warning("DB not connected — showing demo data.")
    st.dataframe(df_c)

# TAB: Analytics & Impact
with tab_analytics:
    st.header("📊 Analytics & Visualizations")

    # Container for all 3 graphs
    with st.container():
        st.markdown("### Key Metrics Overview")
        col1, col2, col3 = st.columns(3)

        # Column 1: AI Opportunity Status Pie Chart
        status_counts = df_ops['status'].value_counts() if not df_ops.empty else pd.Series()
        fig1, ax1 = plt.subplots(figsize=(3,2.5))
        if not status_counts.empty:
            ax1.pie(status_counts, labels=status_counts.index, autopct="%1.1f%%", startangle=90)
        ax1.set_title("AI Opportunity Status", fontsize=10)
        col1.pyplot(fig1)

        # Column 2: Campaign Sent vs Converted Bar
        if not df_c.empty:
            fig2, ax2 = plt.subplots(figsize=(3,2.5))
            ax2.bar(["Sent", "Converted"], [len(df_c), df_c['click_count'].sum() if 'click_count' in df_c.columns else 0], color=['skyblue', 'orange'])
            ax2.set_ylabel("Count", fontsize=8)
            ax2.set_title("Campaigns Sent vs Converted", fontsize=10)
            col2.pyplot(fig2)

        # Column 3: Agent Impact
        fig3, ax3 = plt.subplots(figsize=(3,2.5))
        ax3.bar(["Baseline", "Live Agent"], [BASELINE_RATE, success_rate], color=['gray', 'green'], width=0.35)
        ax3.set_ylim(0, max(BASELINE_RATE, success_rate)*1.2)
        ax3.set_yticks([])  # hide y-axis
        ax3.set_xticks([0,1])
        ax3.set_xticklabels(["Baseline", "Live Agent"], fontsize=8)
        ax3.set_title("Agent Impact", fontsize=10)
        for i, v in enumerate([BASELINE_RATE, success_rate]):
            ax3.text(i, v + 0.3, f"{v}%", ha='center', fontsize=8)
        plt.tight_layout()
        col3.pyplot(fig3)
