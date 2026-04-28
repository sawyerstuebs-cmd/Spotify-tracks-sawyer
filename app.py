import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="FATAL SYNCHRONIZATION", page_icon="🎧", layout="wide")

# 2. Advanced Animation CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Share+Tech+Mono&display=swap');

        /* Tactical Slate Background */
        .stApp {
            background-color: #0d1117;
            color: #ffffff;
        }

        /* 🌀 ANIMATION: Spinning Vinyl Record */
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        .spotify-vinyl {
            width: 80px;
            animation: spin 3s linear infinite;
            filter: drop-shadow(0 0 10px #1DB954);
        }

        /* 🔥 ANIMATION: Pulsing Energy Bars */
        @keyframes pulse {
            0% { opacity: 0.5; transform: scaleX(0.9); }
            50% { opacity: 1; transform: scaleX(1.1); }
            100% { opacity: 0.5; transform: scaleX(0.9); }
        }
        .energy-bar {
            height: 4px;
            background: linear-gradient(90deg, #FF6600, #A065D4, #00FFFF);
            margin: 10px 0;
            animation: pulse 2s ease-in-out infinite;
        }

        /* Typography */
        h1, h2, .section-header {
            font-family: 'Orbitron', sans-serif !important;
            text-transform: uppercase;
        }
        p, span, label, .stMetric {
            font-family: 'Share Tech Mono', monospace !important;
        }

        .section-header {
            font-size: 1.1rem;
            color: #FFCC00;
            border-left: 5px solid #A065D4;
            padding-left: 15px;
            background: rgba(255, 255, 255, 0.05);
        }

        /* Character Container */
        .battle-stage {
            display: flex;
            justify-content: space-around;
            align-items: center;
            background: rgba(0,0,0,0.3);
            border-bottom: 2px solid #FF0033;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# 3. TOP ANIMATION BAR (The Battle Stage)
st.markdown("""
    <div class="battle-stage">
        <img src="https://www.fightersgeneration.com/characters4/scorpion-classic-stance.gif" height="100">
        <div style="text-align: center;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" class="spotify-vinyl">
            <div style="color: #1DB954; font-weight: bold; margin-top: 5px;">LIVE_STREAM_SYNC</div>
        </div>
        <img src="https://www.fightersgeneration.com/characters4/subzero-classic-stance.gif" height="100">
    </div>
    <div class="energy-bar"></div>
""", unsafe_allow_html=True)

# 4. Data Loading
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("tracks.csv")
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        return df
    except Exception as e:
        st.error(f"FATALITY: System Error {e}")
        return pd.DataFrame()

df_raw = load_data()

# 5. Dashboard Logic
if not df_raw.empty:
    genre_col = 'track_genre' if 'track_genre' in df_raw.columns else df_raw.columns[0]
    
    # Sidebar
    st.sidebar.markdown("<h2 style='color:#FF6600;'>COMMAND_CENTER</h2>", unsafe_allow_html=True)
    pilot_name = st.sidebar.text_input("IDENTIFY PILOT:", "Goku_SubZero")
    
    all_genres = sorted(df_raw[genre_col].unique().astype(str))
    selected_genres = st.sidebar.multiselect("GENRE_REALM:", all_genres, default=all_genres[0:2])
    
    # Filter Data
    df = df_raw[df_raw[genre_col].isin(selected_genres)]
    
    # Header
    st.markdown(f"<h1 style='text-align:center; color:#00FFFF;'>{pilot_name}'S AUDIO KOMBAT</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#FFCC00;'>SYNCING TRACK DATA... KI LEVELS STABLE.</p>", unsafe_allow_html=True)

    # 6. Metrics with Glow
    st.markdown('<p class="section-header">CORE_METRICS</p>', unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    m1.metric("TRACK_COUNT", len(df))
    m2.metric("AVG_POWER (POP)", f"{df['popularity'].mean():.1f}")
    m3.metric("SYNC_RATE (DANCE)", f"{df['danceability'].mean()*100:.1f}%")

    # 7. Animated Visuals (Charts)
    st.divider()
    c1, c2 = st.columns(2)
    
    # Palette: Purple, Orange, Cyan, Yellow
    custom_colors = ["#A065D4", "#FF6600", "#00FFFF", "#FFCC00"]

    with c1:
        fig1 = px.scatter(df, x="danceability", y="popularity", color=genre_col, 
                         title="SONIC_KINETICS (DANCE vs POWER)",
                         color_discrete_sequence=custom_colors)
        fig1.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.05)')
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        feat_avg = df.groupby(genre_col)[["energy", "danceability"]].mean().reset_index()
        fig2 = px.bar(feat_avg, x=genre_col, y=["energy", "danceability"], barmode="group",
                     title="WAVEFORM_ENERGY_DISTRIBUTION",
                     color_discrete_sequence=["#FF0033", "#00FFFF"])
        fig2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.05)')
        st.plotly_chart(fig2, use_container_width=True)

    # 8. Data Archive
    st.markdown('<p class="section-header">DATA_LOG_FILES</p>', unsafe_allow_html=True)
    st.dataframe(df.head(20), use_container_width=True)
    
    # Moving Footer Animation
    st.markdown('<div class="energy-bar"></div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:0.7rem;'>ALL DATA RETRIEVED FROM NERV/CAPSULE_CORP SERVERS</p>", unsafe_allow_html=True)

else:
    st.warning("AWAITING DATA INPUT... INSERT TRACKS.CSV")
