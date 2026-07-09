import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

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
    .main {
        background-color: #f7f9fc;
    }

    .title-box {
        background-color: #0b1f3a;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 20px;
    }

    .title-box h1 {
        color: white;
        margin: 0;
        font-size: 36px;
    }

    .title-box p {
        color: #dbe7f3;
        margin-top: 8px;
        font-size: 17px;
    }

    .metric-card {
        background-color: white;
        padding: 22px;
        border-radius: 14px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 6px solid #0b1f3a;
    }

    .section-title {
        font-size: 24px;
        font-weight: 700;
        color: #0b1f3a;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .footer-note {
        color: #6b7280;
        font-size: 13px;
        margin-top: 18px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div class="title-box">
    <h1>A&E Waiting Room Monitoring Dashboard</h1>
    <p>Prototype front-desk interface for wearable-based patient escalation monitoring.</p>
</div>
""", unsafe_allow_html=True)

patients = ["P001", "P002", "P003", "P004", "P005", "P006"]

placeholder = st.empty()

def generate_patient_data():
    patient_data = []

    for patient in patients:
        heart_rate = random.randint(65, 140)
        movement_level = round(random.uniform(0.1, 4.0), 2)

        score = 0

        if heart_rate >= 120:
            score += 3
        elif heart_rate >= 100:
            score += 2

        if movement_level >= 3.0:
            score += 2
            movement_status = "Restless"
        elif movement_level <= 0.3:
            score += 1
            movement_status = "Very low movement"
        else:
            movement_status = "Normal"

        if score >= 5:
            status = "Urgent reassessment"
            action = "Prioritize immediately"
        elif score >= 3:
            status = "Review suggested"
            action = "Nurse reassessment"
        else:
            status = "Stable"
            action = "Continue monitoring"

        patient_data.append({
            "Patient ID": patient,
            "Heart Rate": f"{heart_rate} bpm",
            "Movement": movement_status,
            "Status": status,
            "Action": action
        })

    return pd.DataFrame(patient_data)

def highlight_status(row):
    if row["Status"] == "Urgent reassessment":
        return ["background-color: #f8d7da; color: #721c24; font-weight: 600"] * len(row)
    elif row["Status"] == "Review suggested":
        return ["background-color: #fff3cd; color: #856404; font-weight: 600"] * len(row)
    else:
        return ["background-color: #d4edda; color: #155724"] * len(row)

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
            st.metric("Total Monitored", total_count)

        with col2:
            st.metric("Stable", stable_count)

        with col3:
            st.metric("Need Review", review_count)

        with col4:
            st.metric("Urgent", urgent_count)

        if urgent_count > 0:
            st.error("Urgent reassessment required. One or more patients should be prioritized immediately.")
        elif review_count > 0:
            st.warning("Review suggested. One or more patients may require nurse reassessment.")
        else:
            st.success("All monitored patients are currently stable.")

        st.markdown('<div class="section-title">Live Patient Status</div>', unsafe_allow_html=True)
        st.caption(f"Last updated: {last_updated}")

        styled_df = df.style.apply(highlight_status, axis=1)
        st.dataframe(styled_df, use_container_width=True, hide_index=True)

        st.markdown("""
        <div class="footer-note">
            Prototype system for feasibility demonstration only. Status indicators are generated from simulated heart-rate and movement data.
        </div>
        """, unsafe_allow_html=True)

    time.sleep(2)
