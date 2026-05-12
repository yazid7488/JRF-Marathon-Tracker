import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Jakarta 2026 Tracker", layout="centered")

st.title("🏃 Jakarta Marathon '26")
st.subheader("Goal: 4:30:00 (Pace: 6:24)")

@st.cache_data
def load_data():
    try:
        df = pd.read_excel("Jakarta_Marathon_High_Volume_Plan.xlsx")
        return df
    except Exception as e:
        st.error(f"Error loading Excel: {e}")
        return None

df = load_data()

if df is not None:
    selected_week_label = st.selectbox("Current Training Week:", df['Week'])
    week_idx = df.index[df['Week'] == selected_week_label][0]
    
    progress = (week_idx + 1) / len(df)
    st.progress(progress)

    tab1, tab2, tab3 = st.tabs(["📅 Today", "📊 Plan", "⏱️ Paces"])

    with tab1:
        week_data = df.iloc[week_idx]
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for day in days:
            with st.expander(f"{day}: {week_data[day][:25]}..."):
                st.write(week_data[day])
                st.checkbox("Done", key=f"{selected_week_label}_{day}")

    with tab2:
        st.dataframe(df[['Week', 'Date', 'Sunday', 'Total Vol']], use_container_width=True)

    with tab3:
        st.metric("Marathon Pace", "6:24-6:30")
        st.metric("Tempo Pace", "6:15-6:25")
        st.metric("Easy Pace", "7:10-7:30")
