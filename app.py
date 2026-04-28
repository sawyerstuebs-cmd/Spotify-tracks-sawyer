import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="NEO-TOKYO ANALYTICS", page_icon="💊", layout="wide")

# 2. Akira x Cyber-Saiyan CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Share+Tech+Mono&display=swap');

        /* 🌆 AKIRA GRID BACKGROUND */
        .stApp {
            background-color: #050505;
            background-image: 
                linear-gradient(0deg, transparent 24%, rgba(0, 255, 255, .05) 25%, rgba(0, 255, 255, .05) 26%, transparent 27%, transparent 74%, rgba(0, 255, 255, .05) 75%, rgba(0, 255, 255, .05) 76%, transparent 77%, transparent),
                linear-gradient(90deg, transparent 24%, rgba(0, 255, 255, .05) 25%, rgba(0, 255, 255, .05) 26%, transparent 27%, transparent 74%, rgba(0, 255, 255, .05) 75%, rgba(0, 255, 255, .05) 76%, transparent 77%, transparent);
            background-size: 50px 50px;
            color: #ffffff;
        }

        /* 🌀 ANIMATION: Spinning Spotify Vinyl */
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        .spotify-vinyl {
            width: 70px;
            animation: spin 3s linear infinite;
            filter: drop-shadow(0 0 10px #FF0000);
        }

        /* 🚨 EMERGENCY PROTOCOL ANIMATION */
        @keyframes flicker {
            0% { opacity: 1; }
            50% { opacity: 0.4; }
            100% { opacity: 1; }
        }
        .emergency-header {
            color: #FF0000;
            font-family: 'Orbitron', sans-serif;
            text-shadow: 0 0 15px #FF0000;
            animation: flicker 0.5s infinite;
            text-align: center;
            font-size: 3rem;
            margin-bottom: 0px;
        }

        /* Typography */
        h1, h2, .section-header {
            font-family: 'Orbitron', sans-serif !important;
        }
        p, span, label, .stMetric {
            font-family: 'Share Tech Mono', monospace !important;
        }

        .section-header {
            font-size: 1.1rem;
            color: #00FFFF;
            border-left: 5px solid #FF0000;
            padding-left: 15px;
            background: rgba(255, 0, 0, 0.1);
            margin: 20px 0;
        }

        /* Battle Stage Overlay */
        .battle-stage {
            display: flex;
            justify-content: space-around;
            align-items: center;
            background: rgba(0,0,0,0.6);
            border-bottom: 3px solid #FF0000;
            padding: 15px;
            box-shadow: 0 10px 20px rgba(255,0,0,0.2);
        }
    </style>
""", unsafe_allow_html=True)

# 3. TOP ANIMATION BAR (The Neo-Tokyo Stage)
st.markdown("""
    <div class="battle-stage">
        <img src="https://www.fightersgeneration.com/characters4/scorpion-classic-stance.gif" height="100">
        <div>
            <div class="emergency-header">警告</div>
            <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" class="spotify-vinyl" style="display: block; margin: auto;">
        </div>
        <img src="https://www.fightersgeneration.com/characters4/subzero-classic-stance.gif" height="100">
    </div>
""", unsafe_allow_html=True)

# 4. Data Loading
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("tracks.csv")
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        return df
    except Exception as e:
        st.error(f"SYSTEM OVERLOAD: {e}")
        return pd.DataFrame()

df_raw = load_data()

# 5. Dashboard Logic
if not df_raw.empty:
    genre_col = 'track_genre' if 'track_genre' in df_raw.columns else df_raw.columns[0]
    
    # Sidebar - Capsule Corp / NERV style
    st.sidebar.markdown("<h2 style='color:#FF0000;'>SYSTEM_SETTINGS</h2>", unsafe_allow_html=True)
    pilot_name = st.sidebar.text_input("PILOT_ID:", "KANEDA_01")
    
    all_genres = sorted(df_raw[genre_col].unique().astype(str))
    selected_genres = st.sidebar.multiselect("GENRE_SECTOR:", all_genres, default=all_genres[0:2])
    
    # Filter Data
    df = df_raw[df_raw[genre_col].isin(selected_genres)]
    
    # Header
    st.markdown(f"<h1 style='text-align:center; color:#ffffff;'>{pilot_name} // AUDIO_KOMBAT</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#00FFFF;'>GRID_STATUS: ACTIVE // POWER_LEVEL: STABLE</p>", unsafe_allow_html=True)

    # 6. Metrics (Scouter Display)
    st.markdown('<p class="section-header">REAL_TIME_ANALYSIS</p>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("TRACK_NODES", len(df))
    m2.metric("AVG_POWER", f"{df['popularity'].mean():.1f}")
    m3.metric("SYNC_RATIO", f"{df['danceability'].mean()*100:.1f}%")
    m4.metric("KI_ENERGY", f"{df['energy'].mean()*100:.1f}%")

    # 7. Neon Charts
    st.divider()
    c1, c2 = st.columns(2)
    
    # Akira Palette: Red, White, Cyan, Yellow
    akira_colors = ["#FF0000", "#FFFFFF", "#00FFFF", "#FFCC00"]

    with c1:
        fig1 = px.scatter(df, x="danceability", y="popularity", color=genre_col, 
                         title="KINETIC_SYNC (DANCE/POWER)",
                         color_discrete_sequence=akira_colors)
        fig1.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.05)')
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        feat_avg = df.groupby(genre_col)[["energy", "danceability"]].mean().reset_index()
        fig2 = px.bar(feat_avg, x=genre_col, y=["energy", "danceability"], barmode="group",
                     title="AUDIO_WAVEFORM_ENERGY",
                     color_discrete_sequence=["#FF0000", "#00FFFF"])
        fig2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.05)')
        st.plotly_chart(fig2, use_container_width=True)

    # 8. Data Archive
    st.markdown('<p class="section-header">NERV_ARCHIVE_LOGS</p>', unsafe_allow_html=True)
    st.dataframe(df.head(15), use_container_width=True)
    
    st.markdown("<p style='text-align:center; font-size:0.7rem; color:#444;'>NEO-TOKYO IS ABOUT TO EXPLODE</p>", unsafe_allow_html=True)

else:
    st.warning("AWAITING TRACKS.CSV UPLOAD...")
