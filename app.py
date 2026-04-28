import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="NEO-TOKYO KOMBAT", page_icon="💊", layout="wide")

# 2. Ultra-Hybrid Animation CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Share+Tech+Mono&display=swap');

        /* 🌆 AKIRA GRID + NEON BACKGROUND */
        .stApp {
            background-color: #000000;
            background-image: 
                linear-gradient(0deg, transparent 24%, rgba(0, 255, 255, .15) 25%, rgba(0, 255, 255, .15) 26%, transparent 27%, transparent 74%, rgba(0, 255, 255, .15) 75%, rgba(0, 255, 255, .15) 76%, transparent 77%, transparent),
                linear-gradient(90deg, transparent 24%, rgba(0, 255, 255, .15) 25%, rgba(0, 255, 255, .15) 26%, transparent 27%, transparent 74%, rgba(0, 255, 255, .15) 75%, rgba(0, 255, 255, .15) 76%, transparent 77%, transparent);
            background-size: 60px 60px;
            box-shadow: inset 0 0 100px rgba(0, 255, 255, 0.2);
            color: #ffffff;
        }

        /* 🌀 KAMEHAMEHA ENERGY BEAM ANIMATION */
        @keyframes beam-glow {
            0% { width: 0px; opacity: 0; box-shadow: 0 0 0px #00FFFF; }
            20% { width: 400px; opacity: 1; box-shadow: 0 0 30px #00FFFF; }
            80% { width: 400px; opacity: 1; box-shadow: 0 0 50px #00FFFF; }
            100% { width: 0px; opacity: 0; }
        }
        .beam {
            height: 20px;
            background: white;
            border-radius: 10px;
            display: inline-block;
            vertical-align: middle;
            animation: beam-glow 4s infinite;
            box-shadow: 0 0 20px #00FFFF;
        }

        /* Spinning Vinyl */
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        .spotify-vinyl {
            width: 60px;
            animation: spin 3s linear infinite;
            filter: drop-shadow(0 0 15px #FF0000);
            vertical-align: middle;
        }

        /* Emergency Header */
        @keyframes flicker { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
        .emergency-header {
            color: #FF0000;
            font-family: 'Orbitron', sans-serif;
            text-shadow: 0 0 20px #FF0000;
            animation: flicker 0.7s infinite;
            text-align: center;
            font-size: 2.5rem;
        }

        /* Battle Stage Overlay */
        .battle-stage {
            display: flex;
            justify-content: space-around;
            align-items: center;
            background: rgba(0,0,0,0.8);
            border-bottom: 4px solid #FF0000;
            padding: 15px;
            box-shadow: 0 10px 30px rgba(255,0,0,0.4);
        }

        /* Typography */
        h1, h2, .section-header { font-family: 'Orbitron', sans-serif !important; }
        p, span, label, [data-testid="stMetricValue"] { font-family: 'Share Tech Mono', monospace !important; }

        .section-header {
            font-size: 1.2rem;
            color: #00FFFF;
            border-left: 6px solid #FF0000;
            padding-left: 15px;
            background: rgba(255, 0, 0, 0.2);
            margin: 20px 0;
        }
    </style>
""", unsafe_allow_html=True)

# 3. THE KAMEHAMEHA BATTLE STAGE
st.markdown("""
    <div class="battle-stage">
        <img src="https://www.fightersgeneration.com/characters4/scorpion-classic-stance.gif" height="90">
        
        <div style="white-space: nowrap;">
            <img src="https://www.icegif.com/wp-content/uploads/icegif-2244.gif" height="100" style="vertical-align: middle; transform: scaleX(-1);">
            <div class="beam"></div>
            <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" class="spotify-vinyl">
        </div>

        <img src="https://www.fightersgeneration.com/characters4/subzero-classic-stance.gif" height="90">
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
    
    # Sidebar
    st.sidebar.markdown("<h2 style='color:#FF0000;'>SYSTEM_SETTINGS</h2>", unsafe_allow_html=True)
    pilot_name = st.sidebar.text_input("PILOT_ID:", "GOKU_KANEDA")
    
    all_genres = sorted(df_raw[genre_col].unique().astype(str))
    selected_genres = st.sidebar.multiselect("GENRE_SECTOR:", all_genres, default=all_genres[0:2])
    df = df_raw[df_raw[genre_col].isin(selected_genres)]
    
    # Header
    st.markdown(f"<h1 style='text-align:center; color:#ffffff;'>{pilot_name} // FINAL_BATTLE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#00FFFF;'>SYNCING KI LEVELS... KAMEHAMEHA CHARGED.</p>", unsafe_allow_html=True)

    # 6. Metrics
    st.markdown('<p class="section-header">SCROLLING_COMBAT_DATA</p>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("TRACK_POWER", len(df))
    m2.metric("AVG_KI_LVL", f"{df['popularity'].mean():.1f}")
    m3.metric("SYNC_RATE", f"{df['danceability'].mean()*100:.1f}%")
    m4.metric("ENERGY_RESERVE", f"{df['energy'].mean()*100:.1f}%")
    
    st.markdown("<style>[data-testid='stMetricValue'] { color: #00FF66 !important; text-shadow: 0 0 10px #00FF66; }</style>", unsafe_allow_html=True)

    # 7. Neon Charts
    st.divider()
    c1, c2 = st.columns(2)
    akira_colors = ["#FF0000", "#FFFFFF", "#00FFFF", "#FFCC00"]

    with c1:
        fig1 = px.scatter(df, x="danceability", y="popularity", color=genre_col, 
                         title="KINETIC_SYNC", color_discrete_sequence=akira_colors)
        fig1.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        feat_avg = df.groupby(genre_col)[["energy", "danceability"]].mean().reset_index()
        fig2 = px.bar(feat_avg, x=genre_col, y=["energy", "danceability"], barmode="group",
                     title="ENERGY_WAVEFORM", color_discrete_sequence=["#FF0000", "#00FFFF"])
        fig2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)

    # 8. Raw Data
    st.markdown('<p class="section-header">NERV_HIDDEN_FILES</p>', unsafe_allow_html=True)
    st.dataframe(df.head(10), use_container_width=True)

else:
    st.error("IT'S OVER 9000 ERRORS! Check tracks.csv.")
