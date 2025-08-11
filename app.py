import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from PIL import Image

# Page setup
st.set_page_config(page_title="SpaceX Launches", layout="wide")

# Load SpaceX logo
try:
    logo = Image.open("spacex.png")
    st.image(logo, width=300)
except:
    st.title("🚀 SpaceX Launch Tracker")

# Load data function
@st.cache_data
def get_launch_data():
    launches = requests.get("https://api.spacexdata.com/v4/launches").json()
    rockets = {r['id']: r['name'] for r in requests.get("https://api.spacexdata.com/v4/rockets").json()}
    launchpads = {l['id']: l['name'] for l in requests.get("https://api.spacexdata.com/v4/launchpads").json()}
    
    simple_data = []
    for launch in launches:
        try:
            simple_data.append({
                "Mission": launch['name'],
                "Date": datetime.fromisoformat(launch['date_utc'][:-1]).strftime('%Y-%m-%d'),
                "Rocket": rockets.get(launch['rocket'], "Unknown"),
                "Launch Site": launchpads.get(launch['launchpad'], "Unknown"),
                "Success": "✅" if launch['success'] else "❌"
            })
        except:
            continue
    
    return pd.DataFrame(simple_data)

# Get the data
df = get_launch_data().sort_values("Date", ascending=False)

# Dashboard Title
st.header("🚀Recent SpaceX Launches")

# Show latest 10 launches
st.dataframe(
    df.head(10),
    column_config={
        "Mission": "Mission Name",
        "Date": "Launch Date", 
        "Rocket": "Rocket Type",
        "Launch Site": "Launch Location",
        "Success": "Status"
    },
    use_container_width=True,
    hide_index=True
)

# Add some statistics
st.subheader("Launch Statistics")

col1, col2, col3 = st.columns(3)
col1.metric("Total Launches", len(df))
col2.metric("Success Rate", f"{len(df[df['Success'] == '✅'])/len(df)*100:.1f}%")
col3.metric("Unique Rockets", df['Rocket'].nunique())

# Simple chart of launches by year
st.subheader("Launches by Year")
year_counts = df['Date'].str[:4].value_counts().sort_index()
st.bar_chart(year_counts)

# Footer
st.markdown("---")
st.caption("Data from SpaceX API | Updated automatically")