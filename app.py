import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="NIGHT CITY ANALYTICS", page_icon="🏙️", layout="wide")

# 2. Cyberpunk Glassmorphism & High-Contrast CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Share+Tech+Mono&family=Vt323&display=swap');

        /* 🏙️ DYNAMIC CYBERPUNK BACKGROUND */
        .stApp {
            background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
                        url('https://images.unsplash.com/photo-1605806616949-1e87b487fc2f?q=80&w=2070&auto=format&fit=crop');
            background-size: cover;
            background-attachment: fixed;
            color: #ffffff;
        }

        /* 🧪 GLASSMORPHISM CONTAINERS - Makes data pop over bright backgrounds */
        [data-testid="stMetric"], .stDataFrame, .stPlotlyChart {
            background: rgba(0, 0, 0, 0.7) !important;
            border: 1px solid rgba(0, 255, 255, 0.3);
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.1);
        }

        /* 🌀 ANIMATION: Neon Spinning Spotify Vinyl */
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        .spotify-vinyl {
            width: 80px;
            animation: spin 3s linear infinite;
            filter: drop-shadow(0 0 15px #FF00FF); /* Hot Pink Glow */
        }

        /* 🚨 EMERGENCY HEADER (NERV/Edgerunners Style) */
        @keyframes flicker { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
        .emergency-header {
            color: #FF0033;
            font-family: 'Orbitron', sans-serif;
            text-shadow: 0 0 20px #FF0033;
            animation: flicker 0.8s infinite;
            text-align: center;
            font-size: 3.5rem;
        }

        /* Typography */
        h1, h2, .section-header {
            font-family: 'Orbitron', sans-serif !important;
            text-shadow: 2px 2px 10px rgba(0, 255, 255, 0.5);
        }

        .section-header {
            font-size: 1.2rem;
            color: #00FFFF;
            border-left: 6px solid #FF00FF;
            background: rgba(255, 0, 255, 0.1);
            padding: 10px 20px;
            margin: 25px 0;
        }

        /* Battle Stage Overlay */
        .battle-stage {
            display: flex;
            justify-content: space-around;
            align-items: center;
            background: rgba(0,0,0,0.85);
            border-bottom: 4px solid #00FFFF;
            padding: 20px;
            box-shadow: 0 10px 40px rgba(0, 255, 255, 0.3);
        }

        /* Custom Metric Text */
        [data-testid="stMetricValue"] {
            color: #00FF66 !important;
            text-shadow: 0 0 10px #00FF66;
            font-family: 'Vt323', monospace !important;
            font-size: 2.5rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# 3. TOP ANIMATION BAR (The Cyber-Stage)
st.markdown("""
    <div class="battle-stage">
        <img src="https://www.fightersgeneration.com/characters4/scorpion-classic-stance.gif" height="110">
        <div>
            <div class="emergency-header">警告_SYSTEM_HOT</div>
            <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" class="spotify-vinyl" style="display: block; margin: auto;">
        </div>
        <img src="https://www.fightersgeneration.com/characters4/subzero-classic-stance.gif" height="110">
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
        st.error(f"FATALITY: {e}")
        return pd.DataFrame()

df_raw = load_data()

# 5. Dashboard Logic
if not df_raw.empty:
    genre_col = 'track_genre' if 'track_genre' in df_raw.columns else df_raw.columns[0]
    name_col = 'track_name' if 'track_name' in df_raw.columns else df_raw.columns[1]
    
    # Sidebar - Edgerunners Chrome
    st.sidebar.markdown("<h2 style='color:#00FFFF;'>CHOOM_CONFIG</h2>", unsafe_allow_html=True)
    pilot_name = st.sidebar.text_input("NETRUNNER_ID:", "DAVID_MARTINEZ_01")
    
    all_genres = sorted(df_raw[genre_col].unique().astype(str))
    selected_genres = st.sidebar.multiselect("GENRE_REALM:", all_genres, default=all_genres[0:2])
    df = df_raw[df_raw[genre_col].isin(selected_genres)]
    
    # Main Header
    st.markdown(f"<h1 style='text-align:center; color:#ffffff;'>{pilot_name} // NEURAL_KOMBAT</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#00FFFF;'>STATUS: CHROMED // LOCATION: NIGHT CITY</p>", unsafe_allow_html=True)

    # 6. Metrics
    st.markdown('<p class="section-header">SCOUTER_DATA_FEED</p>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("NODES", f"{len(df):,}")
    m2.metric("POWER", f"{df['popularity'].mean():.1f}")
    m3.metric("SYNC", f"{df['danceability'].mean()*100:.1f}%")
    m4.metric("KI_ENERGY", f"{df['energy'].mean()*100:.1f}%")

    # 7. Neon Charts
    st.divider()
    c1, c2 = st.columns(2)
    cyber_palette = ["#00FFFF", "#FF00FF", "#A065D4", "#FF6600"]

    with c1:
        fig1 = px.scatter(df, x="danceability", y="popularity", color=genre_col, 
                         title="KINETIC_SYNC", color_discrete_sequence=cyber_palette)
        fig1.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        top_df = df.sort_values("popularity", ascending=False).head(15)
        fig2 = px.bar(top_df, x=name_col, y=["energy", "danceability"], barmode="group",
                     title="WAVEFORM_ENERGY", color_discrete_sequence=["#FF00FF", "#00FFFF"]) 
        fig2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_tickangle=-45)
        st.plotly_chart(fig2, use_container_width=True)

    # 8. Data Archive
    st.markdown('<p class="section-header">ENCRYPTED_LOGS</p>', unsafe_allow_html=True)
    st.dataframe(df.head(15), use_container_width=True)
    
    st.markdown("<br><p style='text-align:center; font-size:0.8rem; color:#888;'>'Wake up Samurai, we have a playlist to analyze.'</p>", unsafe_allow_html=True)

else:
    st.error("ERROR: NO DATA DETECTED. CHECK tracks.csv.")
