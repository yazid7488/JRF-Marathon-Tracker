import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Jakarta Marathon Tracker", layout="wide")

# Custom CSS for UI and Color Coding
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .summary-card { background-color: #1a1c24; padding: 15px; border-radius: 12px; border: 1px solid #333; text-align: center; }
    .day-card { background-color: #1e1e26; border-radius: 10px; padding: 12px; margin-bottom: 10px; min-height: 110px; border-left: 5px solid; }
    
    /* Phase Badges */
    .phase-badge { padding: 2px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: bold; }
    
    /* Specific Run Type Colors */
    .color-easy { border-left-color: #2ECC71 !important; }      /* Green */
    .color-tempo { border-left-color: #F1C40F !important; }     /* Yellow */
    .color-progressive { border-left-color: #E67E22 !important; }/* Orange */
    .color-interval { border-left-color: #9B59B6 !important; }   /* Purple */
    .color-long { border-left-color: #E74C3C !important; }       /* Red */
    .color-rest { border-left-color: #95A5A6 !important; }       /* Grey */
    </style>
""", unsafe_allow_html=True)

# 1. Dashboard Header (Top Cards)
st.title("🏃 Jakarta '26 Dashboard")
col_top1, col_top2, col_top3 = st.columns(3)

# Initialized to "Zero" or "TBD" as requested
with col_top1:
    st.markdown('<div class="summary-card"><p style="color:#888;margin:0;">Week No</p><h2 style="margin:0;">0</h2></div>', unsafe_allow_html=True)
with col_top2:
    st.markdown('<div class="summary-card"><p style="color:#888;margin:0;">Today\'s Workout</p><h2 style="margin:0;">-</h2></div>', unsafe_allow_html=True)
with col_top3:
    st.markdown('<div class="summary-card"><p style="color:#888;margin:0;">Target Long Run</p><h2 style="margin:0;">0 km</h2></div>', unsafe_allow_html=True)

# 2. Data Loading
@st.cache_data
def load_data():
    df = pd.read_excel("Jakarta_Marathon_High_Volume_Plan_v2.xlsx")
    return df

df = load_data()

# 3. Helper for Color Coding
def get_style_class(text):
    text = text.lower()
    if "long" in text: return "color-long"
    if "interval" in text: return "color-interval"
    if "tempo" in text: return "color-tempo"
    if "progression" in text or "progressive" in text: return "color-progressive"
    if "rest" in text: return "color-rest"
    return "color-easy"

# 4. Weekly View
for idx, row in df.iterrows():
    # Phase logic: BUILD (Green), PEAK (Red), TAPER (Blue)
    phase_name = row['Phase']
    phase_color = row['PhaseColor']
    
    label = f"**{row['Week']}** | {row['Date']} | {row['Total Vol']}"
    
    with st.expander(label):
        st.markdown(f'<span class="phase-badge" style="background-color:{phase_color};">{phase_name}</span>', unsafe_allow_html=True)
        
        # Grid layout for mobile (Monday - Thursday)
        days = ["Monday", "Tuesday", "Wednesday", "Thursday"]
        for i in range(0, 4, 2):
            cols = st.columns(2)
            for j in range(2):
                day = days[i+j]
                content = str(row[day])
                st_class = get_style_class(content)
                cols[j].markdown(f'<div class="day-card {st_class}"><b>{day[:3]}</b><br>{content}</div>', unsafe_allow_html=True)
                cols[j].checkbox("Done", key=f"c_{idx}_{day}")

        # Friday Special (AM/PM separation)
        st.markdown("---")
        st.write("Friday Double Session")
        f_cols = st.columns(2)
        f_content = str(row["Friday"])
        am_part = f_content.split("/")[0] if "/" in f_content else "AM: 5km Easy"
        pm_part = f_content.split("/")[1] if "/" in f_content else "PM: Intervals"
        
        with f_cols[0]:
            st.markdown(f'<div class="day-card color-easy"><b>FRI AM</b><br>{am_part}</div>', unsafe_allow_html=True)
            st.checkbox("AM Done", key=f"c_{idx}_fam")
        with f_cols[1]:
            st.markdown(f'<div class="day-card color-interval"><b>FRI PM</b><br>{pm_part}</div>', unsafe_allow_html=True)
            st.checkbox("PM Done", key=f"c_{idx}_fpm")
            
        # Weekend
        st.markdown("---")
        w_cols = st.columns(2)
        with w_cols[0]:
            st.markdown(f'<div class="day-card color-rest"><b>SAT</b><br>{row["Saturday"]}</div>', unsafe_allow_html=True)
        with w_cols[1]:
            st_class_sun = get_style_class(str(row["Sunday"]))
            st.markdown(f'<div class="day-card {st_class_sun}"><b>SUN</b><br>{row["Sunday"]}</div>', unsafe_allow_html=True)
            st.checkbox("LR Done", key=f"c_{idx}_sun")
