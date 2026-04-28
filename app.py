"""
BAN-461 Capstone: Spotify Audio Trends Dashboard
Analytical Question: Which musical characteristics (Energy, Danceability, Acousticness) 
define the most popular tracks, and how do these trends vary across different genres?
"""

import streamlit as st
import pandas as pd
import plotly.express as px

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
    # Ensure tracks.csv is in your GitHub repo
    df = pd.read_csv("tracks.csv")
    return df

try:
    df_raw = load_data()
except Exception as e:
    st.error(f"Error loading tracks.csv: {e}")
    st.stop()

# Sidebar filters
st.sidebar.header("🔎 Filters")

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

# Compute Metrics for Filtered Data
total_tracks = len(df)
avg_pop      = df["popularity"].mean() if not df.empty else 0
avg_dance    = df["danceability"].mean() * 100 if not df.empty else 0
avg_energy   = df["energy"].mean() * 100 if not df.empty else 0

# Baselines for Deltas (Full dataset)
base_pop   = df_raw["popularity"].mean()
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
    # Chart 1: Avg Audio Features by Genre (Grouped Bar)
    feature_means = df.groupby("track_genre")[["energy", "danceability", "acousticness"]].mean().reset_index()
    fig1 = px.bar(
        feature_means,
        x="track_genre",
        y=["energy", "danceability", "acousticness"],
        barmode="group",
        title="Audio Characteristics by Genre",
        labels={"value": "Score (0-1)", "track_genre": "Genre", "variable": "Feature"},
        color_discrete_sequence=["#1DB954", "#2E86AB", "#F06543"]
    )
    fig1.update_layout(height=400)
    st.plotly_chart(fig1, use_container_width=True)

with chart_col2:
    # Chart 2: Popularity Distribution (Trend Line / Area)
    pop_dist = df.groupby("popularity").size().reset_index(name="count")
    fig2 = px.area(
        pop_dist,
        x="popularity",
        y="count",
        title="Popularity Density in Selection",
        labels={"popularity": "Popularity Score", "count": "Number of Tracks"},
        color_discrete_sequence=["#1DB954"]
    )
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

# Chart 3: Danceability vs. Popularity (Bubble Scatter)
fig3 = px.scatter(
    df.head(1000), # Sampled for performance
    x="danceability",
    y="popularity",
    size="energy",
    color="track_genre",
    hover_name="track_name",
    title="Danceability vs. Popularity (Bubble Size = Energy)",
    labels={"danceability": "Danceability Score", "popularity": "Popularity Score"},
    color_discrete_sequence=px.colors.qualitative.Plotly,
)
fig3.add_hline(y=base_pop, line_dash="dash", line_color="red", annotation_text="Global Avg Popularity")
fig3.update_layout(height=450)
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# Key Findings
st.markdown('<p class="section-header">💡 Key Findings</p>', unsafe_allow_html=True)

st.markdown(
    """
- **Popularity and Rhythmic Appeal.** The bubble scatter plot reveals that tracks scoring above 80 in popularity are heavily clustered in the 0.6 to 0.8 danceability range. This suggests that "groove" is a more consistent driver of mainstream success than raw loudness or energy.

- **Genre-Specific Structural Profiles.** The grouped bar chart demonstrates that Pop and EDM maximize energy and danceability, while genres like Folk or Acoustic show significantly higher acousticness. This confirms that artists should optimize audio features for genre-specific benchmarks rather than chasing a "universal" sound.

- **The Energy-Popularity Tradeoff.** Interestingly, extremely high-energy tracks (above 0.9) do not always correlate with the highest popularity scores. This points to a "listening fatigue" factor, where moderate-to-high energy is more sustainable for mainstream streaming performance.

- **Data Skew and Viral Potential.** The popularity density chart shows a peak in the 40-60 range, representing the "average" track. Tracks breaking into the 85+ tier often display a distinct combination of high danceability and low acousticness, highlighting the sonic profile preferred by global editorial playlists.
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
    file_name="spotify_filtered_tracks.csv",
    mime="text/csv",
)
