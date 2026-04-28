import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page config
st.set_page_config(page_title="Cyberpunk Spotify Analytics", page_icon="⚡", layout="wide")

# 2. Cyberpunk Neon CSS
st.markdown("""
    <style>
        /* Main background and text */
        .stApp {
            background-color: #0d0d0d;
            color: #e0e0e0;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #1a1a1a;
            border-right: 1px solid #FF00FF;
        }
        
        /* Section headers with Neon Glow */
        .section-header {
            font-size: 1.2rem;
            font-weight: 800;
            color: #00FFFF; /* Cyan */
            text-transform: uppercase;
            letter-spacing: 2px;
            border-bottom: 1px solid #FF00FF; /* Magenta */
            padding-bottom: 5px;
            margin-bottom: 15px;
            text-shadow: 0 0 10px #00FFFF, 0 0 20px #00FFFF;
        }

        /* Metric Styling */
        [data-testid="stMetricValue"] {
            color: #FF00FF !important;
            font-family: 'Courier New', Courier, monospace;
        }
        
        /* Custom Divider */
        hr {
            border: 0;
            height: 1px;
            background-image: linear-gradient(to right, #00FFFF, #FF00FF, transparent);
        }
    </style>
""", unsafe_allow_html=True)

# 3. Data loading with Error Handling
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("tracks.csv")
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        return df
    except Exception as e:
        st.error(f"SYSTEM ERROR: Data Link Severed: {e}")
        return pd.DataFrame()

df_raw = load_data()

# 4. Filter logic
if not df_raw.empty:
    genre_col = 'track_genre' if 'track_genre' in df_raw.columns else df_raw.columns[0]

    # Sidebar
    st.sidebar.markdown("<h2 style='color:#FF00FF;'>USER_INTERFACE</h2>", unsafe_allow_html=True)
    user_name = st.sidebar.text_input("IDENTIFY USER:", placeholder="NEXUS-6")

    all_genres = sorted(df_raw[genre_col].unique().astype(str))
    selected_genres = st.sidebar.multiselect("FILTER_GENRE", options=all_genres, default=all_genres[0:3])
    pop_range = st.sidebar.slider("POPULARITY_LEVEL", 0, 100, (40, 100))

    # Apply filters
    df = df_raw[df_raw[genre_col].isin(selected_genres)]
    df = df[df["popularity"].between(pop_range[0], pop_range[1])]

    # 5. Header
    st.markdown("<h1 style='color: #00FFFF; text-align: center; text-shadow: 2px 2px #FF00FF;'>NEURAL SPOTIFY NETWORK</h1>", unsafe_allow_html=True)
    
    if user_name:
        st.markdown(f"<p style='text-align: center; color: #FF00FF;'>WELCOME TO THE GRID, <b>{user_name.upper()}</b></p>", unsafe_allow_html=True)
    
    st.markdown("<p style='text-align: center; font-style: italic;'>'All those tracks will be lost in time, like tears in rain...'</p>", unsafe_allow_html=True)
    st.divider()

    # 6. Neon KPIs
    st.markdown('<p class="section-header">DATA_STREAMS</p>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("NODES_DETECTED", f"{len(df):,}")
    k2.metric("AVG_POPULARITY", f"{df['popularity'].mean():.1f}" if not df.empty else "0")
    k3.metric("DANCEABILITY", f"{df['danceability'].mean()*100:.1f}%" if 'danceability' in df.columns else "0%")
    k4.metric("ENERGY_RESERVE", f"{df['energy'].mean()*100:.1f}%" if 'energy' in df.columns else "0%")

    # 7. Neon Visualizations
    st.divider()
    col1, col2 = st.columns(2)

    # Custom Cyberpunk Colors
    neon_colors = ["#00FFFF", "#FF00FF", "#FFFF00", "#00FF00", "#FF0000"]

    with col1:
        if 'danceability' in df.columns:
            fig1 = px.scatter(df, x="danceability", y="popularity", color=genre_col, 
                             title="SYNC_ANALYSIS: DANCE vs POP",
                             color_discrete_sequence=neon_colors)
            fig1.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig1, use_container_width=True)

    with col2:
        if 'energy' in df.columns:
            feat_means = df.groupby(genre_col)[["energy", "danceability"]].mean().reset_index()
            fig2 = px.bar(feat_means, x=genre_col, y=["energy", "danceability"], barmode="group",
                         title="OUTPUT_SPECTRUM: ENERGY/DANCE", 
                         color_discrete_sequence=["#FF00FF", "#00FFFF"])
            fig2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig2, use_container_width=True)

    # 8. Data Table
    st.divider()
    st.markdown('<p class="section-header">RAW_LOG_FILES</p>', unsafe_allow_html=True)
    # Styling the dataframe with dark theme
    st.dataframe(df.head(50).style.set_properties(**{'background-color': '#1a1a1a', 'color': '#00FFFF', 'border-color': '#FF00FF'}))
else:
    st.error("ACCESS DENIED: tracks.csv not found in main directory.")
