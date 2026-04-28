import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="NEURAL KOMBAT GRID", page_icon="🎧", layout="wide")

# 2. Ultra-Hybrid Aesthetic CSS
st.markdown("""
    <style>
        /* FONTS: Heavy contrast for Edgerunners/NGE tactical feel */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Share+Tech+Mono&family=Vt323&display=swap');

        /* 🌌 BACKGROUND OVERLOAD: NGE Slate, Edgerunners Black, Saiyan Orange Grid */
        .stApp {
            /* Deep Space/Slate Background */
            background-color: #0d1117;
            
            /* NEON Saiyan Gridlines (Orange) */
            background-image: 
                linear-gradient(0deg, transparent 24%, rgba(255, 102, 0, .08) 25%, rgba(255, 102, 0, .08) 26%, transparent 27%, transparent 74%, rgba(255, 102, 0, .08) 75%, rgba(255, 102, 0, .08) 76%, transparent 77%, transparent),
                linear-gradient(90deg, transparent 24%, rgba(255, 102, 0, .08) 25%, rgba(255, 102, 0, .08) 26%, transparent 27%, transparent 74%, rgba(255, 102, 0, .08) 75%, rgba(255, 102, 0, .08) 76%, transparent 77%, transparent);
            background-size: 50px 50px;
            
            color: #ffffff;
            font-family: 'Share Tech Mono', monospace;
        }

        /* 🌀 ANIMATION: Spinning Spotify Vinyl with Saiyan Glow */
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        .spotify-vinyl {
            width: 80px;
            animation: spin 3s linear infinite;
            filter: drop-shadow(0 0 15px #FF6600); /* Saiyan Orange Glow */
        }

        /* 🚨 EMERGENCY PROTOCOL ANIMATION (NGE Red) */
        @keyframes flicker {
            0% { opacity: 1; }
            50% { opacity: 0.3; }
            100% { opacity: 1; }
        }
        .emergency-header {
            color: #FF0033; /* NERV Red */
            font-family: 'Orbitron', sans-serif;
            text-shadow: 0 0 15px #FF0033, 0 0 25px #FF0033;
            animation: flicker 0.6s infinite;
            text-align: center;
            font-size: 3rem;
            margin-bottom: 0px;
        }

        /* Typography Overhaul */
        h1, h2, .section-header {
            font-family: 'Orbitron', sans-serif !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 0 0 8px rgba(255,255,255,0.5);
        }
        
        p, span, label, .stMetric {
            font-family: 'Share Tech Mono', monospace !important;
        }

        /* Section Header: Eva Purple/Saiyan Orange Hybrid */
        .section-header {
            font-size: 1.1rem;
            color: #FFCC00; /* Nimbus Yellow */
            border-left: 6px solid #A065D4; /* Eva-01 Purple */
            background: linear-gradient(90deg, #FF6600, transparent); /* Saiyan Orange */
            padding: 8px 15px;
            margin: 20px 0;
            box-shadow: 0 0 15px rgba(160, 101, 212, 0.4);
        }

        /* Battle Stage Overlay (Kept but refined) */
        .battle-stage {
            display: flex;
            justify-content: space-around;
            align-items: center;
            background: rgba(0,0,0,0.8);
            border-bottom: 4px solid #FF0033; /* NERV Red Border */
            padding: 15px;
            box-shadow: 0 10px 30px rgba(255,0,0,0.3);
            margin-top: -1rem;
        }
        
        /* Sidebar styling for Edgerunners/NGE Chrome look */
        [data-testid="stSidebar"] {
            background-color: #0a0c10;
            border-right: 3px solid #A065D4; /* Eva Purple */
            box-shadow: 5px 0 20px rgba(160, 101, 212, 0.2);
        }
    </style>
""", unsafe_allow_html=True)

# 3. TOP ANIMATION BAR (The Hybrid Battle Stage)
st.markdown("""
    <div class="battle-stage">
        <img src="https://www.fightersgeneration.com/characters4/scorpion-classic-stance.gif" height="100">
        <div>
            <div class="emergency-header">警告_EMERGENCY</div>
            <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" class="spotify-vinyl" style="display: block; margin: auto;">
            <div style="color: #00FF66; font-family:'Vt323', monospace; text-align:center; margin-top:5px;">SENSING_KI...</div>
        </div>
        <img src="https://www.fightersgeneration.com/characters4/subzero-classic-stance.gif" height="100">
    </div>
""", unsafe_allow_html=True)

# 4. Data Loading
@st.cache_data
def load_data():
    try:
        # Assumes tracks.csv is present
        df = pd.read_csv("tracks.csv")
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        return df
    except Exception as e:
        st.error(f"SYSTEM OVERLOAD: Dragon Balls Scattered: {e}")
        return pd.DataFrame()

df_raw = load_data()

# 5. Dashboard Logic
if not df_raw.empty:
    genre_col = 'track_genre' if 'track_genre' in df_raw.columns else df_raw.columns[0]
    name_col = 'track_name' if 'track_name' in df_raw.columns else ('track_title' if 'track_title' in df_raw.columns else df_raw.columns[1])
    
    # Sidebar - Edgerunners/Capsule Corp style
    st.sidebar.markdown("<h2 style='color:#FF0033;'>SYSTEM_SETTINGS</h2>", unsafe_allow_html=True)
    pilot_name = st.sidebar.text_input("IDENTIFY_PILOT (User Name):", "Goku_Vegeta_01")
    
    all_genres = sorted(df_raw[genre_col].unique().astype(str))
    selected_genres = st.sidebar.multiselect("GENRE_REALM_SECTOR:", all_genres, default=all_genres[0:2])
    df = df_raw[df_raw[genre_col].isin(selected_genres)]
    
    # Header Section
    st.markdown(f"<h1 style='text-align:center; color:#ffffff; font-size:3rem;'>{pilot_name} // NEURAL_KOMBAT</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#FF6600;'>GRID_STATUS: ACTIVE // POWER_LEVEL: OVER 9,000</p>", unsafe_allow_html=True)

    # 6. Metrics (Scouter Display - Bright Scouter Green)
    st.markdown('<p class="section-header">SCOUTER_DATA_READOUT</p>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    
    # Colors for Scouter-Green text
    scouter_green = "#00FF66"
    
    m1.metric(label="TRACK_NODES", value=f"{len(df):,}")
    m2.metric(label="AVG_POPULARITY", value=f"{df['popularity'].mean():.1f}")
    m3.metric(label="SYNC_RATE (DANCE)", f"{df['danceability'].mean()*100:.1f}%")
    m4.metric(label="KI_ENERGY (ENERGY)", value=f"{df['energy'].mean()*100:.1f}%")
        
    st.markdown(f"""
        <style>
            [data-testid="stMetricValue"] {{
                color: {scouter_green} !important;
                text-shadow: 0 0 10px {scouter_green};
                font-family: 'Vt323', monospace;
                font-size: 2rem;
            }}
        </style>
    """, unsafe_allow_html=True)

    # 7. Neon Charts
    st.divider()
    c1, c2 = st.columns(2)
    
    # Hybrid Palette: Eva Purple, Saiyan Orange, Cyan, LCL Yellow, Blood Red
    hybrid_palette = ["#A065D4", "#FF6600", "#00FFFF", "#FFCC00", "#FF0033"]

    with c1:
        # Scatter Plot - Kinetic Sync (Dance vs Popularity)
        fig1 = px.scatter(df, x="danceability", y="popularity", color=genre_col, 
                         title="KINETIC_SYNC (DANCE/POWER)",
                         color_discrete_sequence=hybrid_palette)
        # NGE-Style transparent chart with bright accents
        fig1.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.05)', font_color="#ffffff", title_font_color="#A065D4")
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        # Bar Chart - Top Songs by Energy & Danceability
        top_df = df.sort_values("popularity", ascending=False).head(15)
        
        # Eva-01 vs NERV Emergency Colors
        fig2 = px.bar(top_df, x=name_col, y=["energy", "danceability"], barmode="group",
                     title="ENERGY_WAVEFORM_BY_TRACK",
                     color_discrete_sequence=["#FF6600", "#A065D4"]) 
        fig2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.05)', font_color="#ffffff", title_font_color="#A065D4", xaxis_tickangle=-45)
        st.plotly_chart(fig2, use_container_width=True)

    # 8. Data Archive
    st.markdown('<p class="section-header">Z-FIGHTER / MAGI_ARCHIVES</p>', unsafe_allow_html=True)
    st.dataframe(df.head(15), use_container_width=True)
    
    # Moving Footer Animation
    st.markdown('<div style="height:4px; background:linear-gradient(90deg, #A065D4, #FF6600, #FF0033); animation:pulse 2s infinite;"></div>', unsafe_allow_html=True)
    st.markdown("<br><p style='text-align:center; font-size:0.8rem; color:#666; font-family: Vt323, monospace;'>ALL TRACKS WILL BE LOST IN TIME... LIKE TEARS IN RAIN. // CHROME_SYNC: COMPLETED</p>", unsafe_allow_html=True)

    # Adding the pulse animation via inline style inject
    st.markdown("""<style> @keyframes pulse { 0% { opacity: 0.5; } 50% { opacity: 1; } 100% { opacity: 0.5; } } </style>""", unsafe_allow_html=True)

else:
    st.error("round 1: FAILED. system online. tracks.csv check required.")
