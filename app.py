import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="NIGHT CITY ANALYTICS", page_icon="🏙️", layout="wide")

# 2. Cyberpunk Glassmorphism & Neon UI CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Share+Tech+Mono&family=Vt323&display=swap');

        /* 🏙️ DYNAMIC CYBERPUNK CITY BACKGROUND */
        .stApp {
            background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                        url('https://images.unsplash.com/photo-1605806616949-1e87b487fc2f?q=80&w=2070&auto=format&fit=crop');
            background-size: cover;
            background-attachment: fixed;
            color: #ffffff;
        }

        /* 🧪 GLASSMORPHISM CONTAINERS */
        [data-testid="stMetric"], .stDataFrame, .stPlotlyChart {
            background: rgba(0, 0, 0, 0.8) !important;
            border: 1px solid rgba(0, 255, 255, 0.4);
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
        }

        /* 🌀 ANIMATION: Neon Spinning Spotify Vinyl */
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        .spotify-vinyl {
            width: 70px;
            animation: spin 3s linear infinite;
            filter: drop-shadow(0 0 15px #FF00FF);
        }

        /* 🚨 EMERGENCY HEADER Flicker */
        @keyframes flicker { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
        .emergency-header {
            color: #FF0033;
            font-family: 'Orbitron', sans-serif;
            text-shadow: 0 0 20px #FF0033;
            animation: flicker 0.8s infinite;
            text-align: center;
            font-size: 2.5rem;
        }

        h1, h2, .section-header {
            font-family: 'Orbitron', sans-serif !important;
            text-shadow: 2px 2px 10px rgba(0, 255, 255, 0.5);
        }

        .section-header {
            font-size: 1.1rem;
            color: #00FFFF;
            border-left: 6px solid #FF00FF;
            background: rgba(255, 0, 255, 0.15);
            padding: 10px 20px;
            margin: 20px 0;
        }

        .battle-stage {
            display: flex;
            justify-content: space-around;
            align-items: center;
            background: rgba(0,0,0,0.9);
            border-bottom: 4px solid #00FFFF;
            padding: 20px;
            box-shadow: 0 10px 40px rgba(0, 255, 255, 0.4);
        }

        [data-testid="stMetricValue"] {
            color: #00FF66 !important;
            text-shadow: 0 0 10px #00FF66;
            font-family: 'Vt323', monospace !important;
            font-size: 2.2rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# 3. TOP ANIMATION BAR (Battle Stage)
st.markdown("""
    <div class="battle-stage">
        <img src="https://www.fightersgeneration.com/characters4/scorpion-classic-stance.gif" height="100">
        <div>
            <div class="emergency-header">警告_TRACK_LOADED</div>
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
        st.error(f"SYSTEM FAILURE: {e}")
        return pd.DataFrame()

df_raw = load_data()

# 5. Dashboard Logic
if not df_raw.empty:
    # Column identification
    genre_col = 'track_genre' if 'track_genre' in df_raw.columns else df_raw.columns[0]
    name_col = 'track_name' if 'track_name' in df_raw.columns else df_raw.columns[1]
    
    # Sidebar - Individual Song Selection
    st.sidebar.markdown("<h2 style='color:#00FFFF;'>TRACK_SELECTOR</h2>", unsafe_allow_html=True)
    pilot_id = st.sidebar.text_input("NETRUNNER_ID:", "DAVID_MARTINEZ_01")
    
    # Sort titles and allow selection
    all_tracks = sorted(df_raw[name_col].unique().astype(str))
    selected_tracks = st.sidebar.multiselect(
        "SELECT_TARGET_SONGS:", 
        options=all_tracks, 
        default=all_tracks[0:5] if len(all_tracks) > 5 else all_tracks
    )
    
    # Filter by chosen titles
    df = df_raw[df_raw[name_col].isin(selected_tracks)]
    
    # Main Header
    st.markdown(f"<h1 style='text-align:center; color:#ffffff;'>{pilot_id} // AUDIO_KOMBAT</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#00FFFF;'>STATUS: TARGETING_TRACKS // GRID: STABLE</p>", unsafe_allow_html=True)

    # 6. Metrics
    st.markdown('<p class="section-header">TARGET_DATA_FEED</p>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("TRACKS", len(df))
    m2.metric("AVG_POWER", f"{df['popularity'].mean():.1f}" if not df.empty else "0")
    m3.metric("SYNC_RATE", f"{df['danceability'].mean()*100:.1f}%" if not df.empty else "0%")
    m4.metric("KI_ENERGY", f"{df['energy'].mean()*100:.1f}%" if not df.empty else "0%")

    # 7. Neon Charts
    st.divider()
    c1, c2 = st.columns(2)
    cyber_palette = ["#00FFFF", "#FF00FF", "#A065D4", "#FF6600", "#FF0033"]

    with c1:
        # Scatter Plot uses titles as the label
        fig1 = px.scatter(df, x="danceability", y="popularity", 
                         color=name_col, 
                         hover_name=name_col,
                         title="KINETIC_SYNC (TRACK_POSITIONING)", 
                         color_discrete_sequence=cyber_palette)
        fig1.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        # Energy Waveform by specific Title
        fig2 = px.bar(df, x=name_col, y=["energy", "danceability"], barmode="group",
                     title="WAVEFORM_ENERGY_BY_TRACK", 
                     color_discrete_sequence=["#FF00FF", "#00FFFF"]) 
        fig2.update_layout(
            template="plotly_dark", 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_tickangle=-45,
            showlegend=True
        )
        st.plotly_chart(fig2, use_container_width=True)

    # 8. Data Table
    st.markdown('<p class="section-header">CHROMED_ARCHIVE_LOGS</p>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
    
    st.markdown("<br><p style='text-align:center; font-size:0.8rem; color:#888;'>'Never fade away, Netrunner.'</p>", unsafe_allow_html=True)

else:
    st.error("SYSTEM ERROR: Data Link Severed. Ensure tracks.csv is present.")
