import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="A&E Patient Monitoring",
    page_icon="🏥",
    layout="wide"
)

# -----------------------------
# Custom styling
# -----------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #f5f7fb;
    }

    .header-box {
        background: linear-gradient(90deg, #08203e, #0b3d66);
        padding: 28px 32px;
        border-radius: 16px;
        margin-bottom: 24px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.12);
    }

    .header-box h1 {
        color: white;
        font-size: 38px;
        margin: 0;
        font-weight: 800;
    }

    .header-box p {
        color: #dbeafe;
        font-size: 17px;
        margin-top: 8px;
        margin-bottom: 0;
    }

    .status-note {
        background-color: white;
        padding: 14px 18px;
        border-radius: 12px;
        border-left: 5px solid #0b3d66;
        margin-bottom: 18px;
        color: #1f2937;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    .section-title {
        font-size: 24px;
        font-weight: 800;
        color: #08203e;
        margin-top: 18px;
        margin-bottom: 4px;
    }

    .small-text {
        color: #6b7280;
        font-size: 14px;
        margin-bottom: 14px;
    }

    .footer-note {
        color: #6b7280;
        font-size: 13px;
        margin-top: 18px;
        padding-top: 10px;
        border-top: 1px solid #e5e7eb;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        border: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div class="header-box">
    <h1>Emergency Department Patient Monitoring System</h1>
    <p>Prototype front-desk dashboard for wearable-based heart rate and movement monitoring.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="status-note">
    <strong>System mode:</strong> Simulated wearable data &nbsp; | &nbsp;
    <strong>Data source:</strong> ESP32 prototype simulation &nbsp; | &nbsp;
    <strong>Purpose:</strong> Feasibility demonstration
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Patient simulation
# -----------------------------
patients = ["P001", "P002", "P003", "P004", "P005", "P006"]

placeholder = st.empty()

def generate_patient_data():
    patient_data = []

    for patient in patients:
        wait_time = random.randint(5, 95)
        heart_rate = random.randint(65, 140)
        movement_level = round(random.uniform(0.1, 4.0), 2)

        score = 0

        # Heart-rate logic
        if heart_rate >= 120:
            score += 3
        elif heart_rate >= 100:
            score += 2

        # Movement logic
        if movement_level >= 3.0:
            score += 2
            movement_status = "Restless"
        elif movement_level <= 0.3:
            score += 1
            movement_status = "Very low movement"
        else:
            movement_status = "Normal"

        # Final status
        if score >= 5:
            status = "Urgent reassessment"
            action = "Prioritize immediately"
            priority = 1
        elif score >= 3:
            status = "Review suggested"
            action = "Nurse reassessment"
            priority = 2
        else:
            status = "Stable"
            action = "Continue monitoring"
            priority = 3

        patient_data.append({
            "Priority": priority,
            "Patient ID": patient,
            "Wait Time": f"{wait_time} min",
            "Heart Rate": f"{heart_rate} bpm",
            "Movement": movement_status,
            "Status": status,
            "Action": action
        })

    df = pd.DataFrame(patient_data)

    # Sort so urgent patients rise to the top
    df = df.sort_values(by=["Priority", "Patient ID"])

    # Hide internal priority column
    df = df.drop(columns=["Priority"])

    return df

def highlight_status(row):
    if row["Status"] == "Urgent reassessment":
        return [
            "background-color: #f8d7da; color: #721c24; font-weight: 700"
        ] * len(row)
    elif row["Status"] == "Review suggested":
        return [
            "background-color: #fff3cd; color: #856404; font-weight: 700"
        ] * len(row)
    else:
        return [
            "background-color: #d4edda; color: #155724"
        ] * len(row)

# -----------------------------
# Live updating dashboard
# -----------------------------
while True:
    df = generate_patient_data()

    urgent_count = len(df[df["Status"] == "Urgent reassessment"])
    review_count = len(df[df["Status"] == "Review suggested"])
    stable_count = len(df[df["Status"] == "Stable"])
    total_count = len(df)

    last_updated = datetime.now().strftime("%H:%M:%S")

    with placeholder.container():
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Patients Monitored", total_count)

        with col2:
            st.metric("Stable", stable_count)

        with col3:
            st.metric("Need Review", review_count)

        with col4:
            st.metric("Urgent Alerts", urgent_count)

        if urgent_count > 0:
            st.error("Urgent reassessment required. One or more patients should be prioritized immediately.")
        elif review_count > 0:
            st.warning("Review suggested. One or more patients may require nurse reassessment.")
        else:
            st.success("All monitored patients are currently stable.")

        st.markdown('<div class="section-title">Live Patient Status</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="small-text">Last updated: {last_updated} | Auto-refresh interval: 2 seconds</div>',
            unsafe_allow_html=True
        )

        styled_df = df.style.apply(highlight_status, axis=1)

        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True,
            height=300
        )

        st.markdown("""
        <div class="footer-note">
            This dashboard is a prototype for research and feasibility demonstration only.
            Current readings are simulated and are not intended for clinical decision-making.
        </div>
        """, unsafe_allow_html=True)

    time.sleep(2)
