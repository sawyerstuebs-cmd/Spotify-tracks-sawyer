import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page config
st.set_page_config(page_title="Spotify Analytics", page_icon="🎵", layout="wide")

# 2. Professional CSS
st.markdown("""
    <style>
        .block-container { padding-top: 1.5rem; }
        .section-header {
            font-size: 1.1rem; font-weight: 600; color: #1DB954;
            border-bottom: 2px solid #E0E0E0; padding-bottom: 4px; margin-bottom: 12px;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Data loading with Error Handling
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("tracks.csv")
        
        # CRITICAL FIX: Clean column names to prevent KeyErrors
        # This removes hidden spaces and converts 'Track Genre' to 'track_genre'
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return pd.DataFrame()

df_raw = load_data()

# 4. Filter logic with Column Name check
if not df_raw.empty:
    # Check if 'track_genre' exists, if not, try 'genres' or 'genre'
    if 'track_genre' in df_raw.columns:
        genre_col = 'track_genre'
    elif 'genres' in df_raw.columns:
        genre_col = 'genres'
    else:
        genre_col = df_raw.columns[0] # Fallback to first column if all else fails

    # Sidebar
    st.sidebar.header("🔎 Filters")
    user_name = st.sidebar.text_input("Enter your name", placeholder="Your Name")

    all_genres = sorted(df_raw[genre_col].unique().astype(str))
    selected_genres = st.sidebar.multiselect("Music Genres", options=all_genres, default=all_genres[0:3])

    pop_range = st.sidebar.slider("Popularity Range", 0, 100, (40, 100))

    # Apply filters
    df = df_raw[df_raw[genre_col].isin(selected_genres)]
    df = df[df["popularity"].between(pop_range[0], pop_range[1])]

    # 5. Header
    st.title("🎵 Spotify Audio Trends Dashboard")
    if user_name:
        st.markdown(f"### Welcome, {user_name}!")
    
    st.markdown("**Analytical Question:** *Which musical characteristics define the most popular tracks?*")
    st.divider()

    # 6. KPIs
    st.markdown('<p class="section-header">📊 Key Performance Indicators</p>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Tracks in View", f"{len(df):,}")
    k2.metric("Avg Popularity", f"{df['popularity'].mean():.1f}" if not df.empty else "0")
    k3.metric("Avg Danceability", f"{df['danceability'].mean()*100:.1f}%" if 'danceability' in df.columns else "N/A")
    k4.metric("Avg Energy", f"{df['energy'].mean()*100:.1f}%" if 'energy' in df.columns else "N/A")

    # 7. Visualizations
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        if 'danceability' in df.columns:
            fig1 = px.scatter(df, x="danceability", y="popularity", color=genre_col, 
                             title="Danceability vs. Popularity", template="plotly_white")
            st.plotly_chart(fig1, use_container_width=True)

    with col2:
        if 'energy' in df.columns:
            feat_means = df.groupby(genre_col)[["energy", "danceability"]].mean().reset_index()
            fig2 = px.bar(feat_means, x=genre_col, y=["energy", "danceability"], barmode="group",
                         title="Features by Genre", color_discrete_sequence=["#1DB954", "#2E86AB"])
            st.plotly_chart(fig2, use_container_width=True)

    # 8. Data Table
    st.divider()
    st.markdown('<p class="section-header">📋 Filtered Raw Data</p>', unsafe_allow_html=True)
    st.dataframe(df.head(100).reset_index(drop=True), use_container_width=True)
else:
    st.warning("The tracks.csv file could not be read. Check your GitHub repository.")
