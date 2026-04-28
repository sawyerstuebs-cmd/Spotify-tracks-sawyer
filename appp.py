import streamlit as st
st.title('My First Streamlit App')
st.write('Hello! This app is live on Streamlit Community Cloud.')
name = st.text_input('Enter your name:')
if name:
    st.write(f'Welcome, {name}!')

import streamlit as st
import pandas as pd

# 1. Setup the Page
st.set_page_config(page_title="Spotify Analytics", layout="wide")

# 2. Load the Data
@st.cache_data
def load_data():
    # Replace the text inside quotes with the direct link to the CSV
    url = "https://www.kaggle.com/datasets/lehaknarnauli/spotify-datasets/data.csv"
    df = pd.read_csv(url) 
    return df
df = load_data()

# 3. Create the Sidebar Filters
st.sidebar.header("Dashboard Filters")
all_genres = df['track_genre'].unique()
selected_genres = st.sidebar.multiselect("Select Genres", all_genres, default=all_genres[0])

# Apply filters to the data
filtered_df = df[df['track_genre'].isin(selected_genres)]

# 4. Dashboard Title & Metrics
st.title("🎵 Spotify Capstone Dashboard")

col1, col2 = st.columns(2)
col1.metric("Total Songs", len(filtered_df))
col2.metric("Average Popularity", round(filtered_df['popularity'].mean(), 1))

# 5. The Visualization
st.subheader("Danceability vs. Popularity")
fig = px.scatter(
    filtered_df, 
    x="danceability", 
    y="popularity", 
    color="track_genre",
    hover_name="track_name",
    template="plotly_dark"
)
st.plotly_chart(fig, use_container_width=True)

# 6. Data Table
with st.expander("View Filtered Data"):
    st.dataframe(filtered_df)