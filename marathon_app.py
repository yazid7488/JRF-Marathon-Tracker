import streamlit as st
import pandas as pd

st.set_page_config(page_title="Jakarta 2026 Plan", layout="wide")

# Global CSS with fixed Phase Targeting
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    h1 { font-size: 1.3rem !important; margin-bottom: 0px !important; }
    
    /* Force tight spacing between weeks */
    [data-testid="stVerticalBlock"] { gap: 0rem !important; }
    div[data-testid="stVerticalBlockBorderWrapper"] { margin-bottom: -10px !important; }

    /* Day Card Styling - Font size fixed */
    .day-card {
        background-color: #1e1e26;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 8px;
        min-height: 90px;
        border-left: 5px solid;
    }
    .day-card b { font-size: 0.85rem; color: #eee; }
    .day-card p { font-size: 0.8rem; margin: 0; color: #bbb; line-height: 1.3; }
    
    /* Internal padding for expanded view */
    [data-testid="stExpanderDetails"] { padding: 1.2rem 1rem 1rem 1rem !important; }

    /* Phase Specific CSS - Forced by Class */
    .phase-BUILD { border-left: 8px solid #2ECC71 !important; background-color: rgba(46, 204, 113, 0.1) !important; margin-top: 5px; }
    .phase-PEAK { border-left: 8px solid #E74C3C !important; background-color: rgba(231, 76, 60, 0.1) !important; margin-top: 5px; }
    .phase-TAPER { border-left: 8px solid #3498DB !important; background-color: rgba(52, 152, 219, 0.1) !important; margin-top: 5px; }

    /* Run Type Colors */
    .color-easy { border-left-color: #2ECC71 !important; }
    .color-tempo { border-left-color: #F1C40F !important; }
    .color-progressive { border-left-color: #E67E22 !important; }
    .color-interval { border-left-color: #9B59B6 !important; }
    .color-long { border-left-color: #E74C3C !important; }
    .color-rest { border-left-color: #95A5A6 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🏃 Jakarta Marathon '26")

# Dashboard Row
st.markdown("""
    <div style="display: flex; justify-content: space-between; gap: 8px; padding-bottom: 25px; padding-top: 10px;">
        <div style="background:#1a1c24; padding:10px; border-radius:8px; flex:1; text-align:center; border:1px solid #333;">
            <p style="font-size:0.7rem; color:#888; margin:0;">WEEK</p><h3 style="margin:0; font-size:1rem;">0</h3>
        </div>
        <div style="background:#1a1c24; padding:10px; border-radius:8px; flex:1; text-align:center; border:1px solid #333;">
            <p style="font-size:0.7rem; color:#888; margin:0;">TODAY</p><h3 style="margin:0; font-size:1rem;">-</h3>
        </div>
        <div style="background:#1a1c24; padding:10px; border-radius:8px; flex:1; text-align:center; border:1px solid #333;">
            <p style="font-size:0.7rem; color:#888; margin:0;">LONG RUN</p><h3 style="margin:0; font-size:1rem;">0km</h3>
        </div>
    </div>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
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

# Weekly View with Phase-Specific Containers
for idx, row in df.iterrows():
    phase = str(row.get('Phase', 'BUILD')).upper()
    header_text = f"{row['Week']} | {row['Date']} | {row['Total Vol']} | {phase}"
    
    # Wrap each expander in a div with the phase class
    st.markdown(f'<div class="phase-{phase}">', unsafe_allow_html=True)
    with st.expander(header_text):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday"]
        for i in range(0, 4, 2):
            cols = st.columns(2)
            for j in range(2):
                day = days[i+j]
                content = str(row[day])
                st_class = get_style_class(content)
                cols[j].markdown(f'<div class="day-card {st_class}"><b>{day[:3]}</b><p>{content}</p></div>', unsafe_allow_html=True)

        f_cols = st.columns(2)
        f_content = str(row["Friday"])
        am = f_content.split("/")[0].strip() if "/" in f_content else "AM: 5km Easy"
        pm = f_content.split("/")[1].strip() if "/" in f_content else "PM: Intervals"
        f_cols[0].markdown(f'<div class="day-card color-easy"><b>FRI AM</b><p>{am}</p></div>', unsafe_allow_html=True)
        f_cols[1].markdown(f'<div class="day-card color-interval"><b>FRI PM</b><p>{pm}</p></div>', unsafe_allow_html=True)

        w_cols = st.columns(2)
        w_cols[0].markdown(f'<div class="day-card color-rest"><b>SAT</b><p>{row["Saturday"]}</p></div>', unsafe_allow_html=True)
        sun_class = get_style_class(row["Sunday"])
        w_cols[1].markdown(f'<div class="day-card {sun_class}"><b>SUN</b><p>{row["Sunday"]}</p></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
