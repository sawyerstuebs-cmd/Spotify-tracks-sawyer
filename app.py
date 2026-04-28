import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="GALACTIC_KOMBAT_OS", page_icon="🎷", layout="wide")

# 2. THE MEGA-FUSION CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Share+Tech+Mono&family=Vt323&family=Syncopate:wght@700&display=swap');

        /* 🌌 BACKGROUND: Night City Rain x Arrakis Dust x Fhloston Paradise */
        .stApp {
            background: linear-gradient(rgba(0, 0, 0, 0.75), rgba(40, 0, 60, 0.75)), 
                        url('https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?q=80&w=2000&auto=format&fit=crop');
            background-size: cover;
            background-attachment: fixed;
            color: #ffffff;
        }

        /* 💎 THE FIFTH ELEMENT GLOSS: High Saturation & Glass */
        [data-testid="stMetric"], .stDataFrame, .stPlotlyChart {
            background: rgba(10, 10, 10, 0.9) !important;
            border: 3px solid #FF6600; /* Leeloo Orange */
            border-radius: 0px; /* Brutalist Dune Edges */
            padding: 20px;
            box-shadow: 0 0 30px rgba(255, 102, 0, 0.4), inset 0 0 15px rgba(0, 255, 255, 0.2);
        }
        
        /* 🎷 BEBOP SIDEBAR: Jazz-Blue & Gold */
        [data-testid="stSidebar"] {
            background-color: #050510 !important;
            border-right: 4px solid #00FFFF; /* Bebop Neon Blue */
            box-shadow: 10px 0 40px rgba(0, 255, 255, 0.2);
        }
        
        [data-testid="stSidebar"] .stMultiSelect, [data-testid="stSidebar"] .stTextInput {
            background-color: #000000 !important;
            border: 2px solid #FFCC00 !important; /* Arrakis Gold */
        }

        /* 🌀 ANIMATION: Ruby Rhod / Leeloo Spinning Vinyl */
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        .spotify-vinyl {
            width: 90px;
            animation: spin 2s linear infinite;
            filter: drop-shadow(0 0 20px #FF0033); /* Ruby Rhod Red */
        }

        /* 🚨 EMERGENCY HEADER: Multipass x Tyrell Style */
        @keyframes strobe { 0% { color: #FF6600; } 50% { color: #00FFFF; } 100% { color: #FF6600; } }
        .emergency-header {
            font-family: 'Syncopate', sans-serif;
            text-shadow: 0 0 20px #FF6600;
            animation: strobe 1.5s infinite;
            text-align: center;
            font-size: 2.2rem;
            letter-spacing: 10px;
        }

        /* Typography */
        h1, h2, .section-header {
            font-family: 'Orbitron', sans-serif !important;
            text-transform: uppercase;
        }

        .section-header {
            font-size: 1.2rem;
            color: #FFCC00; /* Arrakis Gold */
            border-left: 15px solid #FF6600; /* Leeloo Orange */
            background: linear-gradient(90deg, rgba(255, 102, 0, 0.3), transparent);
            padding: 12px 25px;
            margin: 30px 0;
        }

        .battle-stage {
            display: flex;
            justify-content: space-around;
            align-items: center;
            background: #000000;
            border-bottom: 8px solid #FF0033; /* Fifth Element Red */
            padding: 30px;
            box-shadow: 0 20px 60px rgba(255, 0, 51, 0.5);
        }

        [data-testid="stMetricValue"] {
            color: #00FF66 !important;
            text-shadow: 0 0 15px #00FF66;
            font-family: 'Vt323', monospace !important;
            font-size: 3rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# 3. THE BATTLE STAGE (Multipass x Bebop x Kombat)
st.markdown("""
    <div class="battle-stage">
        <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3NueXpqcXR3bmR3bmR3bmR3bmR3bmR3bmR3bmR3bmR3bmR3bmR3JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/4ilFRqgbzbx4c/giphy.gif" height="120">
        <div>
            <div class="emergency-header">BIG_BADA_BOOM</div>
            <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" class="spotify-vinyl" style="display: block; margin: auto;">
            <p style="color: #FF6600; font-family: 'Share Tech Mono', monospace; text-align: center; margin-top: 10px; letter-spacing: 3px;">LEELOO_DALLAS_MULTIPASS</p>
        </div>
        <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3NueXpqcXR3bmR3bmR3bmR3bmR3bmR3bmR3bmR3bmR3bmR3bmR3JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/ul1omBL2StW8/giphy.gif" height="120">
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
        st.error(f"SYSTEM_OVERLOAD: {e}")
        return pd.DataFrame()

df_raw = load_data()

# 5. Dashboard Logic
if not df_raw.empty:
    name_col = 'track_name' if 'track_name' in df_raw.columns else df_raw.columns[1]
    
    # Sidebar - Bebop Jazz x Dune Spice
    st.sidebar.markdown("<h2 style='color:#00FFFF;'>GALAXY_RADIO_88</h2>", unsafe_allow_html=True)
    pilot_id = st.sidebar.text_input("NETRUNNER / KWISATZ HADERACH:", "KORBEN_DALLAS_99")
    
    all_tracks = sorted(df_raw[name_col].unique().astype(str))
    selected_tracks = st.sidebar.multiselect(
        "SCAN_FREQ_TRACKS:", 
        options=all_tracks, 
        default=all_tracks[0:3] if len(all_tracks) > 3 else all_tracks
    )
    
    df = df_raw[df_raw[name_col].isin(selected_tracks)]
    
    st.markdown(f"<h1 style='text-align:center; color:#ffffff; font-size: 4rem; letter-spacing: -2px;'>{pilot_id} // COSMIC_KOMBAT</h1>", unsafe_allow_html=True)

    # 6. Scouter / Multipass Metrics
    st.markdown('<p class="section-header">STILLSUIT_VITAL_SIGNS</p>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("TRACK_ORBITS", len(df))
    m2.metric("SPICE_LEVEL", f"{df['popularity'].mean():.1f}" if not df.empty else "0")
    m3.metric("SYNC_RATIO", f"{df['danceability'].mean()*100:.1f}%" if not df.empty else "0%")
    m4.metric("ENERGY_KI", f"{df['energy'].mean()*100:.1f}%" if not df.empty else "0%")

    # 7. Neon Charts (The Ruby Rhod Collection)
    st.divider()
    c1, c2 = st.columns(2)
    # The Diva Plavalaguna Palette: Deep Blue, Leeloo Orange, Hot Pink, Arrakis Gold, Bebop Cyan
    diva_palette = ["#0000FF", "#FF6600", "#FF00FF", "#FFCC00", "#00FFFF"]

    with c1:
        fig1 = px.scatter(df, x="danceability", y="popularity", 
                         color=name_col, 
                         hover_name=name_col,
                         title="HYPERSPACE_COORD", 
                         color_discrete_sequence=diva_palette)
        fig1.update_layout(
            template="plotly_dark", 
            paper_bgcolor='#000000', 
            plot_bgcolor='rgba(255,255,255,0.05)',
            font_family="Syncopate",
            xaxis=dict(gridcolor='#222', title="DANCE_COEFFICIENT"),
            yaxis=dict(gridcolor='#222', title="POPULARITY_PULSE")
        )
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        fig2 = px.bar(df, x=name_col, y=["energy", "danceability"], barmode="group",
                     title="AUDIO_PULSE_ANALYSIS", 
                     color_discrete_sequence=["#FF0033", "#00FFFF"]) 
        fig2.update_layout(
            template="plotly_dark", 
            paper_bgcolor='#000000', 
            plot_bgcolor='rgba(255,255,255,0.05)',
            font_family="Share Tech Mono",
            xaxis=dict(tickangle=-45, gridcolor='#111'),
            yaxis=dict(gridcolor='#111')
        )
        st.plotly_chart(fig2, use_container_width=True)

    # 8. Data Archive
    st.markdown('<p class="section-header">ENCRYPTED_MULTIPASS_LOGS</p>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
    
    st.markdown("<br><p style='text-align:center; font-size:0.9rem; color:#FF6600; font-family: Vt323;'>'SEE YOU SPACE COWBOY... THE SPICE MUST FLOW.'</p>", unsafe_allow_html=True)

else:
    st.error("MULTIPASS REJECTED. Check tracks.csv connection.")
