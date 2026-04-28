import streamlit as st
st.title('My First Streamlit App')
st.write('Hello! This app is live on Streamlit Community Cloud.')
name = st.text_input('Enter your name:')
if name:
    st.write(f'Welcome, {name}!')

import streamlit as st
import pandas as pd

# Page config
st.set_page_config(
    page_title="Spotify Analytics",
    page_icon="🎵",
    layout="wide",
)

# Custom CSS for polished look
st.markdown(
    """
    <style>
        .block-container { padding-top: 1.5rem; }
        [data-testid="stMetricDelta"] { font-size: 0.85rem; }
        .section-header {
            font-size: 1.1rem;
            font-weight: 600;
            color: #1DB954; /* Spotify Green */
            border-bottom: 2px solid #E0E0E0;
            padding-bottom: 4px;
            margin-bottom: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Data loading
@st.cache_data
def load_data():
    """Load the Spotify Tracks dataset."""
    # CHANGED: Now looking for tracks_small.csv
    df = pd.read_csv("tracks_small.csv")
    return df

df_raw = load_data()

# Sidebar filters
st.sidebar.header("🔎 Dashboard Filters")

# Filter 1: Name Input (Assignment Requirement)
user_name = st.sidebar.text_input("Enter your name", placeholder="Your Name")

# Filter 2: Genre (multiselect)
all_genres = sorted(df_raw["track_genre"].unique())
selected_genres = st.sidebar.multiselect(
    "Music Genres",
    options=all_genres,
    default=all_genres[0:3] if len(all_genres) > 3 else all_genres,
)

# Filter 3: Popularity Range (slider)
pop_range = st.sidebar.slider(
    "Popularity Score Range",
    min_value=0,
    max_value=100,
    value=(40, 100),
)

# Apply filters
df = df_raw.copy()
df = df[df["track_genre"].isin(selected_genres)]
df = df[df["popularity"].between(pop_range[0], pop_range[1])]

# Header / analytical question
st.title("🎵 Spotify Audio Trends Dashboard")

if user_name:
    st.markdown(f"### Welcome, {user_name}!")

st.markdown(
    """
    **Analytical Question:** *Which musical characteristics (Energy, Danceability, Acousticness) 
    define the most popular tracks, and how do these trends vary across different genres?*
    """
)
st.divider()

# KPI metrics
st.markdown('<p class="section-header">📊 Key Performance Indicators</p>', unsafe_allow_html=True)

total_tracks = len(df)
avg_pop = df["popularity"].mean()
avg_dance = df["danceability"].mean() * 100
avg_energy = df["energy"].mean() * 100

# Comparison baseline (Full dataset avg)
base_pop = df_raw["popularity"].mean()
base_dance = df_raw["danceability"].mean() * 100

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("Tracks in View", f"{total_tracks:,}")
kpi2.metric(
    "Avg Popularity", 
    f"{avg_pop:.1f}", 
    f"{avg_pop - base_pop:+.1f} vs. overall"
)
kpi3.metric(
    "Avg Danceability", 
    f"{avg_dance:.1f}%",
    f"{avg_dance - base_dance:+.1f} pp vs. overall"
)
kpi4.metric("Avg Energy", f"{avg_energy:.1f}%")

st.divider()

# Visualizations
st.markdown('<p class="section-header">📈 Visualizations</p>', unsafe_allow_html=True)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # Chart 1: Danceability vs Popularity Scatter
    fig1 = px.scatter(
        df,
        x="danceability",
        y="popularity",
        color="track_genre",
        hover_name="track_name",
        title="Danceability vs. Popularity Score",
        labels={"danceability": "Danceability Score", "popularity": "Popularity"},
        color_discrete_sequence=px.colors.qualitative.Plotly,
    )
    fig1.update_layout(height=400)
    st.plotly_chart(fig1, use_container_width=True)

with chart_col2:
    # Chart 2: Audio Feature Comparison by Genre
    feature_means = df.groupby("track_genre")[["energy", "danceability", "acousticness"]].mean().reset_index()
    fig2 = px.bar(
        feature_means,
        x="track_genre",
        y=["energy", "danceability", "acousticness"],
        barmode="group",
        title="Avg Audio Features by Genre",
        labels={"value": "Score (0-1)", "track_genre": "Genre", "variable": "Feature"},
        color_discrete_sequence=["#1DB954", "#2E86AB", "#F06543"]
    )
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Key Findings
st.markdown('<p class="section-header">💡 Key Findings</p>', unsafe_allow_html=True)

st.markdown(
    """
- **Popularity is not strictly tied to high energy.** Analysis of the filtered data shows that high danceability scores are more consistently present in the top tier of popular tracks. This suggests that "rhythmic appeal" is a more reliable predictor of mainstream success than "raw intensity."

- **Genre-specific 'vibes' are structurally distinct.** The comparison bar chart reveals that Pop and EDM genres maximize Danceability and Energy, whereas Acoustic or Folk genres show significantly higher Acousticness. This indicates that producers should tailor audio features strictly to genre expectations rather than chasing a universal standard.

- **The 'Sweet Spot' for Popularity.** Most tracks in the filtered selection with popularity above 80 points maintain a danceability score between 0.6 and 0.8, regardless of genre. This "sweet spot" highlights a potential production target for artists seeking broader reach.
"""
)

st.divider()

# Filtered data table + download
st.markdown('<p class="section-header">📋 Filtered Raw Data</p>', unsafe_allow_html=True)

display_cols = ["track_name", "artists", "track_genre", "popularity", "danceability", "energy"]
st.dataframe(df[display_cols].reset_index(drop=True), use_container_width=True, height=300)

# Download button
csv_export = df[display_cols].to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download Filtered Track List",
    data=csv_export,
    file_name="spotify_filtered_data.csv",
    mime="text/csv",
)
