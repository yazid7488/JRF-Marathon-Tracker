import streamlit as st
import pandas as pd

st.set_page_config(page_title="Jakarta 2026 Plan", layout="wide")

# Custom CSS for compact UI, smaller headings, and header badges
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    
    /* Smaller Titles */
    h1 { font-size: 1.2rem !important; margin-bottom: 5px !important; margin-top: 0px !important; }
    
    /* Compact Top Cards in one row */
    .summary-container {
        display: flex;
        justify-content: space-between;
        gap: 8px;
        margin-bottom: 20px;
    }
    .summary-card-mini {
        background-color: #1a1c24;
        padding: 10px 5px;
        border-radius: 8px;
        border: 1px solid #333;
        flex: 1;
        text-align: center;
    }
    .summary-card-mini p { font-size: 0.6rem; color: #888; margin: 0; text-transform: uppercase; }
    .summary-card-mini h3 { font-size: 0.85rem; margin: 0; color: #ffffff; }

    /* Day Card Styling - Optimized for Mobile */
    .day-card {
        background-color: #1e1e26;
        border-radius: 8px;
        padding: 8px;
        margin-bottom: 8px;
        min-height: 80px;
        border-left: 4px solid;
    }
    .day-card b { font-size: 0.75rem; color: #eee; }
    .day-card p { font-size: 0.7rem; margin: 0; color: #bbb; line-height: 1.2; }
    
    /* Phase Badges inside Header (Float right) */
    .phase-badge-inline {
        float: right;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.6rem;
        font-weight: bold;
        color: white;
        margin-left: 10px;
    }

    /* Colors for Run Types */
    .color-easy { border-left-color: #2ECC71 !important; }
    .color-tempo { border-left-color: #F1C40F !important; }
    .color-progressive { border-left-color: #E67E22 !important; }
    .color-interval { border-left-color: #9B59B6 !important; }
    .color-long { border-left-color: #E74C3C !important; }
    .color-rest { border-left-color: #95A5A6 !important; }
    </style>
""", unsafe_allow_html=True)

# 1. Smaller Header
st.title("🏃 Jakarta Marathon '26")

# 2. Compact Top Row
st.markdown("""
    <div class="summary-container">
        <div class="summary-card-mini"><p>Week</p><h3>0</h3></div>
        <div class="summary-card-mini"><p>Today</p><h3>-</h3></div>
        <div class="summary-card-mini"><p>Long Run</p><h3>0km</h3></div>
    </div>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Looks for the v2 file we created with the Phase columns
    return pd.read_excel("Jakarta_Marathon_High_Volume_Plan_v2.xlsx")

df = load_data()

def get_style_class(text):
    text = str(text).lower()
    if "long" in text: return "color-long"
    if "interval" in text: return "color-interval"
    if "tempo" in text: return "color-tempo"
    if "progression" in text or "progressive" in text: return "color-progressive"
    if "rest" in text: return "color-rest"
    return "color-easy"

# 3. Weekly View
for idx, row in df.iterrows():
    phase = row.get('Phase', 'BUILD')
    phase_color = row.get('PhaseColor', '#2ECC71')
    
    header_text = f"{row['Week']} | {row['Date']}"
    
    with st.expander(header_text):
        # Badge added here is visible in the row when expanded or scanned
        st.markdown(f'<span class="phase-badge-inline" style="background-color:{phase_color};">{phase}</span>', unsafe_allow_html=True)
        
        # Mon-Thu Grid
        days = ["Monday", "Tuesday", "Wednesday", "Thursday"]
        for i in range(0, 4, 2):
            cols = st.columns(2)
            for j in range(2):
                day = days[i+j]
                content = str(row[day])
                st_class = get_style_class(content)
                cols[j].markdown(f'<div class="day-card {st_class}"><b>{day[:3]}</b><p>{content}</p></div>', unsafe_allow_html=True)

        # Friday
        st.markdown("<p style='font-size:0.8rem; font-weight:bold; margin-bottom:5px;'>Friday Double</p>", unsafe_allow_html=True)
        f_cols = st.columns(2)
        f_content = str(row["Friday"])
        am = f_content.split("/")[0].strip() if "/" in f_content else "AM: 5km Easy"
        pm = f_content.split("/")[1].strip() if "/" in f_content else "PM: Intervals"
        f_cols[0].markdown(f'<div class="day-card color-easy"><b>FRI AM</b><p>{am}</p></div>', unsafe_allow_html=True)
        f_cols[1].markdown(f'<div class="day-card color-interval"><b>FRI PM</b><p>{pm}</p></div>', unsafe_allow_html=True)

        # Weekend
        w_cols = st.columns(2)
        w_cols[0].markdown(f'<div class="day-card color-rest"><b>SAT</b><p>{row["Saturday"]}</p></div>', unsafe_allow_html=True)
        sun_class = get_style_class(row["Sunday"])
        w_cols[1].markdown(f'<div class="day-card {sun_class}"><b>SUN</b><p>{row["Sunday"]}</p></div>', unsafe_allow_html=True)
