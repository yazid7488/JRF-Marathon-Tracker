import streamlit as st
import pandas as pd

st.set_page_config(page_title="Jakarta Marathon Tracker", layout="wide")

# Custom CSS for the Dark Mode Card Look (matching image.png)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #1a1c24; padding: 15px; border-radius: 12px; border: 1px solid #333; }
    
    /* Day Card Styling */
    .day-card {
        background-color: #1e1e26;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 10px;
        border-left: 5px solid #ff4b4b; /* Default Accent */
        min-height: 120px;
    }
    .day-label { font-size: 0.8rem; color: #888; font-weight: bold; text-transform: uppercase; }
    .type-badge { 
        font-size: 0.7rem; padding: 2px 8px; border-radius: 4px; 
        background: #2d2d3a; color: #00d4ff; font-weight: bold;
    }
    .dist-text { font-size: 1.2rem; font-weight: bold; margin: 5px 0; }
    .pace-text { font-size: 0.8rem; color: #aaa; }
    </style>
""", unsafe_allow_html=True)

# 1. Header Section
st.title("🏃 Jakarta Marathon Tracker")
st.caption("20 weeks • Full 42K • Target: 4:30")

col_h1, col_h2 = st.columns(2)
with col_h1:
    st.button("🏁 25 Oct 2026", use_container_width=True)
with col_h2:
    st.button("🔥 Connect Strava", type="primary", use_container_width=True)

# 2. Data Loading
@st.cache_data
def load_data():
    return pd.read_excel("Jakarta_Marathon_High_Volume_Plan.xlsx")

df = load_data()

# 3. Weekly Accordion Logic (Expand/Hide each week)
for index, row in df.iterrows():
    # Header for each week (W1, W2, etc.) matching image.png style
    week_label = f"{row['Week']} | {row['Date']} | {row['Total Vol']}"
    
    with st.expander(week_label):
        # Create a grid for the cards (2 columns for mobile comfort)
        # Using 2 columns prevents the "cramped" feel of 4 squares across
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        # Split into rows of 2 for better mobile vertical scrolling
        for i in range(0, len(days), 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(days):
                    day_name = days[i+j]
                    content = row[day_name]
                    
                    # Logic to color-code based on run type
                    border_color = "#ff4b4b" if "Long" in content else "#00d4ff"
                    if "Rest" in content: border_color = "#555"
                    
                    with cols[j]:
                        st.markdown(f"""
                            <div class="day-card" style="border-left-color: {border_color};">
                                <div class="day-label">{day_name[:3]}</div>
                                <div class="type-badge">{"REST" if "Rest" in content else "RUN"}</div>
                                <div class="dist-text">{content.split(' ')[0]}</div>
                                <div class="pace-text">{content}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        st.checkbox("Done", key=f"check_{index}_{day_name}")

