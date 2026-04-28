import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Spotify Analytics",
    page_icon="🎵",
    layout="wide",
)

# 2. Custom CSS for Spotify-Themed Styling
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

# 3. Data Loading
@st.cache_data
def load_data():
    """Load the Spotify Tracks dataset."""
    # UPDATED: Changed from tracks_small.csv back to tracks.csv
    df = pd.read_csv("tracks.csv")
    return df

# Initialize data
try:
    df_raw = load_data()
except FileNotFoundError:
    st.error("Error: 'tracks.csv' not found. Please ensure the file is uploaded to your GitHub repository.")
    st.stop()

# 4. Sidebar Filters
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

# 5. Apply Filters
df = df_raw.copy()
df = df[df["track_genre"].isin(selected_genres)]
df = df[df["popularity"].between(pop_range[0], pop_range[1])]

# 6. Header Section
st.title("🎵 Spotify Audio Trends Dashboard")

if user_name:
    st.markdown(f"### Welcome, {user_name}!")
else:
    st.info("Please enter your name in the sidebar to personalize your dashboard.")

st.markdown(
    """
    **Analytical Question:** *Which musical characteristics (Energy, Danceability, Acousticness) 
    define the most popular tracks, and how do these trends vary across different genres?*
    """
)
st.divider()

# 7. KPI Metrics
st.markdown('<p class="section-header">📊 Key Performance Indicators</p>', unsafe_allow_html=True)

if not df.empty:
    total_tracks = len(df)
    avg_pop = df["popularity"].mean()
    avg_dance = df["danceability"].mean() * 100
    avg_energy = df["energy"].mean() * 100

    # Baseline for Comparison
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
else:
    st.warning("No data matches the selected filters.")

st.divider()

# 8. Visualizations
st.markdown('<p class="section-header">📈 Visualizations</p>', unsafe_allow_html=True)

if not df.empty:
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        fig1 = px.scatter(
            df.head(2000), # Sampled for performance
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

    # 9. Key Findings
    st.markdown('<p class="section-header">💡 Key Findings</p>', unsafe_allow_html=True)
    st.markdown(
        """
    - **Popularity is not strictly tied to high energy.** Rhythmic appeal (danceability) is often a more reliable predictor of success than raw intensity.
    - **Genre Identity.** Pop and EDM maximize energy, while Folk and Acoustic show high acousticness—tailoring features to genre expectations is key.
    - **The Sweet Spot.** Tracks with popularity > 80 often sit between 0.6 and 0.8 in danceability.
    """
    )

    st.divider()

    # 10. Filtered Data & Download
    st.markdown('<p class="section-header">📋 Filtered Raw Data</p>', unsafe_allow_html=True)
    display_cols = ["track_name", "artists", "track_genre", "popularity", "danceability", "energy"]
    st.dataframe(df[display_cols].reset_index(drop=True), use_container_width=True, height=300)

    csv_export = df[display_cols].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Filtered Track List",
        data=csv_export,
        file_name="spotify_filtered_data.csv",
        mime="text/csv",
    )
