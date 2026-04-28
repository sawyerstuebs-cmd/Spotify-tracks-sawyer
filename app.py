import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="TYRELL-CAPSULE ANALYTICS", page_icon="🐉", layout="wide")

# 2. Blade Runner x DBZ CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Share+Tech+Mono&family=Vt323&display=swap');

        /* 🌆 MONOLITHIC BACKGROUND: Rainy Night City / Tyrell Corp Vibes */
        .stApp {
            background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), 
                        url('https://images.unsplash.com/photo-1515462277126-2dd0c162007a?q=80&w=2000&auto=format&fit=crop');
            background-size: cover;
            background-attachment: fixed;
            color: #ffffff;
        }

        /* 🏮 SCOUTER-VISION CONTAINERS: Hard Black & Glowing Green Borders */
        [data-testid="stMetric"], .stDataFrame, .stPlotlyChart {
            background: #000000 !important;
            border: 2px solid #00FF66; /* Scouter Green */
            border-radius: 4px; /* Harder edges for industrial feel */
            padding: 20px;
            box-shadow: 0 0 20px rgba(0, 255, 102, 0.2);
        }
        
        /* 🐉 SAIYAN SIDEBAR: Gold and Obsidian */
        [data-testid="stSidebar"] {
            background-color: #050505 !important;
            border-right: 3px solid #FFCC00; /* Super Saiyan Gold */
            box-shadow: 10px 0 30px rgba(255, 204, 0, 0.1);
        }
        
        [data-testid="stSidebar"] .stMultiSelect, [data-testid="stSidebar"] .stTextInput {
            background-color: #000000 !important;
            border: 1px solid #FFCC00 !important;
        }

        /* 🌀 ANIMATION: Dragon Ball 4-Star Spinning Vinyl */
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        .spotify-vinyl {
            width: 80px;
            animation: spin 4s linear infinite;
            filter: drop-shadow(0 0 15px #FF6600); /* Dragon Ball Orange Glow */
        }

        /* 🚨 EMERGENCY HEADER (NGE/Blade Runner Style) */
        @keyframes scanline { 
            0% { transform: translateY(0); }
            100% { transform: translateY(100vh); }
        }
        .emergency-header {
            color: #FFCC00;
            font-family: 'Orbitron', sans-serif;
            text-shadow: 0 0 15px #FFCC00;
            text-align: center;
            font-size: 2.8rem;
            letter-spacing: 5px;
        }

        /* Typography */
        h1, h2, .section-header {
            font-family: 'Orbitron', sans-serif !important;
            text-shadow: 3px 3px #FF0000; /* Blade Runner Red Shadow */
        }

        .section-header {
            font-size: 1.1rem;
            color: #ffffff;
            border-left: 10px solid #FF0000;
            background: rgba(255, 0, 0, 0.1);
            padding: 10px 20px;
            margin: 25px 0;
            text-transform: uppercase;
        }

        .battle-stage {
            display: flex;
            justify-content: space-around;
            align-items: center;
            background: #000000;
            border-bottom: 5px solid #FF0000;
            padding: 25px;
            box-shadow: 0 15px 50px rgba(255, 0, 0, 0.4);
        }

        [data-testid="stMetricValue"] {
            color: #00FF66 !important; /* Scouter Green */
            text-shadow: 0 0 12px #00FF66;
            font-family: 'Vt323', monospace !important;
            font-size: 2.8rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# 3. THE BATTLE STAGE (Tyrell Corp x Capsule Corp)
st.markdown("""
    <div class="battle-stage">
        <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHIxbzF3Ym55Znd4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/ul1omBL2StW8/giphy.gif" height="110">
        <div>
            <div class="emergency-header">OFFWORLD_SYNC_77</div>
            <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" class="spotify-vinyl" style="display: block; margin: auto;">
            <p style="color: #00FF66; font-family: 'Vt323', monospace; text-align: center; margin-top: 10px;">KI_LEVEL: DETECTED</p>
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
        st.error(f"DATA_LINK_SEVERED: {e}")
        return pd.DataFrame()

df_raw = load_data()

# 5. Dashboard Logic
if not df_raw.empty:
    name_col = 'track_name' if 'track_name' in df_raw.columns else df_raw.columns[1]
    
    # Sidebar - Saiyan Gold/Black
    st.sidebar.markdown("<h2 style='color:#FFCC00;'>OFFWORLD_CONFIG</h2>", unsafe_allow_html=True)
    pilot_id = st.sidebar.text_input("REPLICANT_ID / Z-FIGHTER:", "K_OR_GOKU_01")
    
    all_tracks = sorted(df_raw[name_col].unique().astype(str))
    selected_tracks = st.sidebar.multiselect(
        "IDENTIFY_TARGETS:", 
        options=all_tracks, 
        default=all_tracks[0:3] if len(all_tracks) > 3 else all_tracks
    )
    
    df = df_raw[df_raw[name_col].isin(selected_tracks)]
    
    st.markdown(f"<h1 style='text-align:center; color:#ffffff; font-size: 3.5rem;'>{pilot_id} // AUDIO_WARFARE</h1>", unsafe_allow_html=True)

    # 6. Scouter Metrics
    st.markdown('<p class="section-header">TARGET_ACQUISITION_LOG</p>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("TRACK_NODES", len(df))
    m2.metric("POW_LVL", f"{df['popularity'].mean():.1f}" if not df.empty else "0")
    m3.metric("SYNC_RATIO", f"{df['danceability'].mean()*100:.1f}%" if not df.empty else "0%")
    m4.metric("ENERGY_KI", f"{df['energy'].mean()*100:.1f}%" if not df.empty else "0%")

    # 7. Neon Charts (High Contrast Scouter Style)
    st.divider()
    c1, c2 = st.columns(2)
    # The Scouter/Blade Runner Palette: Blood Red, Scouter Green, Neon Cyan, Saiyan Gold
    combat_palette = ["#FF0000", "#00FF66", "#00FFFF", "#FFCC00"]

    with c1:
        fig1 = px.scatter(df, x="danceability", y="popularity", 
                         color=name_col, 
                         hover_name=name_col,
                         title="KINETIC_TRACKING", 
                         color_discrete_sequence=combat_palette)
        fig1.update_layout(
            template="plotly_dark", 
            paper_bgcolor='#000000', 
            plot_bgcolor='#000000',
            font_family="Share Tech Mono",
            xaxis=dict(gridcolor='#1a1a1a', title="SYNC_INDEX"),
            yaxis=dict(gridcolor='#1a1a1a', title="POWER_LEVEL")
        )
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        fig2 = px.bar(df, x=name_col, y=["energy", "danceability"], barmode="group",
                     title="AUDIO_PULSE_ANALYSIS", 
                     color_discrete_sequence=["#FF0000", "#00FF66"]) 
        fig2.update_layout(
            template="plotly_dark", 
            paper_bgcolor='#000000', 
            plot_bgcolor='#000000',
            font_family="Share Tech Mono",
            xaxis=dict(tickangle=-45, gridcolor='#111111'),
            yaxis=dict(gridcolor='#111111')
        )
        st.plotly_chart(fig2, use_container_width=True)

    # 8. Data Archive
    st.markdown('<p class="section-header">ENCRYPTED_TYRELL_FILES</p>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
    
    st.markdown("<br><p style='text-align:center; font-size:0.9rem; color:#555;'>'I've seen things you people wouldn't believe... all those tracks lost in time.'</p>", unsafe_allow_html=True)

else:
    st.error("DATA_LINK_OFFLINE. Check tracks.csv connection.")
