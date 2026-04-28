import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="NIGHT CITY ANALYTICS", page_icon="🏙️", layout="wide")

# 2. Advanced CSS: Purple/Black Sidebar & Neon High-Contrast
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Share+Tech+Mono&family=Vt323&display=swap');

        /* 🏙️ BACKGROUND */
        .stApp {
            background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8)), 
                        url('https://images.unsplash.com/photo-1605806616949-1e87b487fc2f?q=80&w=2070&auto=format&fit=crop');
            background-size: cover;
            background-attachment: fixed;
            color: #ffffff;
        }

        /* 💜 PURPLE NEON SIDEBAR OVERHAUL */
        [data-testid="stSidebar"] {
            background-color: #000000 !important;
            border-right: 2px solid #A065D4;
            box-shadow: 5px 0 15px rgba(160, 101, 212, 0.3);
        }
        
        /* Targets the multiselect and input boxes in the sidebar */
        [data-testid="stSidebar"] .stMultiSelect, [data-testid="stSidebar"] .stTextInput {
            background-color: #1a0033 !important;
            border: 1px solid #A065D4 !important;
            border-radius: 5px;
            color: #ffffff !important;
        }
        
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
            color: #A065D4 !important;
            font-family: 'Orbitron', sans-serif !important;
            text-shadow: 0 0 5px #A065D4;
        }

        /* 🧪 GLASSMORPHISM CONTAINERS - High Contrast Black */
        [data-testid="stMetric"], .stDataFrame, .stPlotlyChart {
            background: #000000 !important; /* Pure Black for maximum contrast */
            border: 2px solid #00FFFF;
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 0 25px rgba(0, 255, 255, 0.2);
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
            border-left: 6px solid #A065D4;
            background: rgba(160, 101, 212, 0.2);
            padding: 10px 20px;
            margin: 20px 0;
        }

        .battle-stage {
            display: flex;
            justify-content: space-around;
            align-items: center;
            background: #000000;
            border-bottom: 4px solid #A065D4;
            padding: 20px;
            box-shadow: 0 10px 40px rgba(160, 101, 212, 0.4);
        }

        [data-testid="stMetricValue"] {
            color: #00FF66 !important;
            text-shadow: 0 0 10px #00FF66;
            font-family: 'Vt323', monospace !important;
            font-size: 2.2rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# 3. TOP ANIMATION BAR
st.markdown("""
    <div class="battle-stage">
        <img src="https://www.fightersgeneration.com/characters4/scorpion-classic-stance.gif" height="100">
        <div>
            <div class="emergency-header">警告_SYNC_LOCKED</div>
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
    name_col = 'track_name' if 'track_name' in df_raw.columns else df_raw.columns[1]
    
    # Sidebar - Purple Neon Track Selector
    st.sidebar.markdown("<h2 style='color:#A065D4;'>TRACK_SELECTOR</h2>", unsafe_allow_html=True)
    pilot_id = st.sidebar.text_input("NETRUNNER_ID:", "DAVID_MARTINEZ_01")
    
    all_tracks = sorted(df_raw[name_col].unique().astype(str))
    selected_tracks = st.sidebar.multiselect(
        "SELECT_TARGET_SONGS:", 
        options=all_tracks, 
        default=all_tracks[0:3] if len(all_tracks) > 3 else all_tracks
    )
    
    df = df_raw[df_raw[name_col].isin(selected_tracks)]
    
    st.markdown(f"<h1 style='text-align:center; color:#ffffff;'>{pilot_id} // AUDIO_KOMBAT</h1>", unsafe_allow_html=True)

    # 6. Metrics
    st.markdown('<p class="section-header">TARGET_DATA_FEED</p>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("TRACKS", len(df))
    m2.metric("AVG_POWER", f"{df['popularity'].mean():.1f}" if not df.empty else "0")
    m3.metric("SYNC_RATE", f"{df['danceability'].mean()*100:.1f}%" if not df.empty else "0%")
    m4.metric("KI_ENERGY", f"{df['energy'].mean()*100:.1f}%" if not df.empty else "0%")

    # 7. Neon Charts - High Contrast
    st.divider()
    c1, c2 = st.columns(2)
    # Brightest Neon Colors for Black Contrast
    cyber_palette = ["#FF00FF", "#00FFFF", "#00FF66", "#FFCC00", "#FF0033"]

    with c1:
        fig1 = px.scatter(df, x="danceability", y="popularity", 
                         color=name_col, 
                         hover_name=name_col,
                         title="KINETIC_POSITIONING", 
                         color_discrete_sequence=cyber_palette)
        # Setting background to solid black and increasing grid line visibility
        fig1.update_layout(
            template="plotly_dark", 
            paper_bgcolor='#000000', 
            plot_bgcolor='#000000',
            xaxis=dict(gridcolor='#333333', zerolinecolor='#555555'),
            yaxis=dict(gridcolor='#333333', zerolinecolor='#555555')
        )
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        fig2 = px.bar(df, x=name_col, y=["energy", "danceability"], barmode="group",
                     title="ENERGY_WAVEFORM", 
                     color_discrete_sequence=["#FF00FF", "#00FFFF"]) 
        fig2.update_layout(
            template="plotly_dark", 
            paper_bgcolor='#000000', 
            plot_bgcolor='#000000',
            xaxis=dict(gridcolor='#333333', tickangle=-45),
            yaxis=dict(gridcolor='#333333')
        )
        st.plotly_chart(fig2, use_container_width=True)

    # 8. Data Table
    st.markdown('<p class="section-header">CHROMED_ARCHIVE_LOGS</p>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
    
    st.markdown("<br><p style='text-align:center; font-size:0.8rem; color:#888;'>'Never fade away, Netrunner.'</p>", unsafe_allow_html=True)

else:
    st.error("SYSTEM ERROR: Data Link Severed.")
