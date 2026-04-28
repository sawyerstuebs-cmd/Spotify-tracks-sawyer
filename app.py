import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="NEO-TOKYO ANALYTICS", page_icon="💊", layout="wide")

# 2. Akira x Cyber-Saiyan x Neon Overload CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Share+Tech+Mono&display=swap');

        /* 🌆 AKIRA GRID + NEON BACKGROUND OVERLOAD */
        .stApp {
            /* Basic Black Background */
            background-color: #000000;
            
            /* NEON GRIDLINES (Cyan) */
            background-image: 
                linear-gradient(0deg, transparent 24%, rgba(0, 255, 255, .15) 25%, rgba(0, 255, 255, .15) 26%, transparent 27%, transparent 74%, rgba(0, 255, 255, .15) 75%, rgba(0, 255, 255, .15) 76%, transparent 77%, transparent),
                linear-gradient(90deg, transparent 24%, rgba(0, 255, 255, .15) 25%, rgba(0, 255, 255, .15) 26%, transparent 27%, transparent 74%, rgba(0, 255, 255, .15) 75%, rgba(0, 255, 255, .15) 76%, transparent 77%, transparent);
            background-size: 60px 60px;
            
            /* ADDING BRIGHT NEON WASH/GLOW OVERLAY */
            box-shadow: inset 0 0 100px rgba(0, 255, 255, 0.2), 
                        inset 0 0 200px rgba(255, 0, 255, 0.1);
            
            color: #ffffff;
        }

        /* 🌀 ANIMATION: Spinning Spotify Vinyl with Red Neon */
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        .spotify-vinyl {
            width: 70px;
            animation: spin 3s linear infinite;
            filter: drop-shadow(0 0 15px #FF0000);
        }

        /* 🚨 EMERGENCY PROTOCOL ANIMATION (Flickering Red) */
        @keyframes flicker {
            0% { opacity: 1; }
            50% { opacity: 0.2; }
            100% { opacity: 1; }
        }
        .emergency-header {
            color: #FF0000;
            font-family: 'Orbitron', sans-serif;
            text-shadow: 0 0 20px #FF0000, 0 0 30px #FF0000;
            animation: flicker 0.7s infinite;
            text-align: center;
            font-size: 3.5rem;
            margin-bottom: 0px;
        }

        /* Typography & General Neon Touches */
        h1, h2, .section-header {
            font-family: 'Orbitron', sans-serif !important;
            color: #ffffff;
            text-shadow: 0 0 10px #ffffff;
        }
        p, span, label, .stMetric {
            font-family: 'Share Tech Mono', monospace !important;
        }

        /* Section Header with Neon Red/Cyan contrast */
        .section-header {
            font-size: 1.2rem;
            color: #00FFFF;
            text-shadow: 0 0 10px #00FFFF;
            border-left: 6px solid #FF0000;
            padding-left: 15px;
            background: rgba(255, 0, 0, 0.2);
            margin: 25px 0;
            box-shadow: 0 0 15px rgba(255,0,0,0.3);
        }

        /* Battle Stage Overlay (Kept but with slightly more glow) */
        .battle-stage {
            display: flex;
            justify-content: space-around;
            align-items: center;
            background: rgba(0,0,0,0.8);
            border-bottom: 4px solid #FF0000;
            padding: 15px;
            box-shadow: 0 10px 30px rgba(255,0,0,0.4);
            margin-top: -1rem; /* Adjusting for Streamlit padding */
        }
        
        /* Sidebar styling for Neon overload */
        [data-testid="stSidebar"] {
            background-color: rgba(10, 10, 10, 0.9);
            border-right: 3px solid #00FFFF;
            box-shadow: 5px 0 20px rgba(0,255,255,0.2);
        }
    </style>
""", unsafe_allow_html=True)

# 3. TOP ANIMATION BAR (The Neo-Tokyo Stage)
st.markdown("""
    <div class="battle-stage">
        <img src="https://www.fightersgeneration.com/characters4/scorpion-classic-stance.gif" height="110">
        <div>
            <div class="emergency-header">警告</div>
            <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" class="spotify-vinyl" style="display: block; margin: auto;">
        </div>
        <img src="https://www.fightersgeneration.com/characters4/subzero-classic-stance.gif" height="110">
    </div>
""", unsafe_allow_html=True)

# 4. Data Loading
@st.cache_data
def load_data():
    try:
        # Assumes tracks.csv is present in the same directory
        df = pd.read_csv("tracks.csv")
        # Standardize columns
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        return df
    except Exception as e:
        st.error(f"SYSTEM OVERLOAD: {e}")
        return pd.DataFrame()

df_raw = load_data()

# 5. Dashboard Logic
if not df_raw.empty:
    genre_col = 'track_genre' if 'track_genre' in df_raw.columns else df_raw.columns[0]
    
    # Sidebar - Capsule Corp / NERV / Neon style
    st.sidebar.markdown("<h2 style='color:#FF0000; text-shadow: 0 0 10px #FF0000;'>SYSTEM_SETTINGS</h2>", unsafe_allow_html=True)
    pilot_name = st.sidebar.text_input("PILOT_ID:", "KANEDA_01")
    
    all_genres = sorted(df_raw[genre_col].unique().astype(str))
    selected_genres = st.sidebar.multiselect("GENRE_SECTOR:", all_genres, default=all_genres[0:2])
    
    # Apply Filter
    df = df_raw[df_raw[genre_col].isin(selected_genres)]
    
    # Main Header with Pilot ID
    st.markdown(f"<h1 style='text-align:center; color:#ffffff;'>{pilot_name} // AUDIO_KOMBAT</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#00FFFF; text-shadow: 0 0 10px #00FFFF;'>GRID_STATUS: ACTIVE // POWER_LEVEL: STABLE</p>", unsafe_allow_html=True)

    # 6. Metrics (Scouter Display - Bright Neon Green)
    st.markdown('<p class="section-header">REAL_TIME_ANALYSIS</p>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    # Custom color for metrics value (Bright Neon Green)
    scouter_green = "#00FF66"
    
    with m1:
        st.metric(label="TRACK_NODES", value=f"{len(df):,}")
    with m2:
        st.metric(label="AVG_POWER", value=f"{df['popularity'].mean():.1f}")
    with m3:
        st.metric(label="SYNC_RATIO", value=f"{df['danceability'].mean()*100:.1f}%")
    with m4:
        st.metric(label="KI_ENERGY", value=f"{df['energy'].mean()*100:.1f}%")
        
    # Injecting the scouter green color specifically into the metric values
    st.markdown(f"""
        <style>
            [data-testid="stMetricValue"] {{
                color: {scouter_green} !important;
                text-shadow: 0 0 10px {scouter_green};
                font-family: 'Share Tech Mono', monospace;
            }}
        </style>
    """, unsafe_allow_html=True)

    # 7. Neon Charts
    st.divider()
    c1, c2 = st.columns(2)
    
    # Akira/Neon Palette: Bright Red, White, Bright Cyan, Bright Yellow
    akira_colors = ["#FF0000", "#FFFFFF", "#00FFFF", "#FFCC00"]

    with c1:
        fig1 = px.scatter(df, x="danceability", y="popularity", color=genre_col, 
                         title="KINETIC_SYNC (DANCE/POWER)",
                         color_discrete_sequence=akira_colors)
        # Layout adjustment for maximum neon visibility
        fig1.update_layout(
            template="plotly_dark", 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', # Transparent to show background grid
            font_color="#ffffff",
            title_font_color="#00FFFF"
        )
        # Adding neon glow to trace borders
        fig1.update_traces(marker=dict(line=dict(width=1, color='#FFFFFF')))
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        feat_avg = df.groupby(genre_col)[["energy", "danceability"]].mean().reset_index()
        fig2 = px.bar(feat_avg, x=genre_col, y=["energy", "danceability"], barmode="group",
                     title="AUDIO_WAVEFORM_ENERGY",
                     color_discrete_sequence=["#FF0000", "#00FFFF"]) # Red and Cyan bars
        fig2.update_layout(
            template="plotly_dark", 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            font_color="#ffffff",
            title_font_color="#00FFFF"
        )
        st.plotly_chart(fig2, use_container_width=True)

    # 8. Data Archive
    st.markdown('<p class="section-header">NERV_ARCHIVE_LOGS</p>', unsafe_allow_html=True)
    # Using default styling but making sure it blends.
    st.dataframe(df.head(15), use_container_width=True)
    
    st.markdown("<br><p style='text-align:center; font-size:0.8rem; color:#666; font-family: monospace;'>NEO-TOKYO IS ABOUT TO EXPLODE // ACCESS_LOG: CLOSED</p>", unsafe_allow_html=True)

else:
    # Error state if file is missing
    st.error("SYSTEM OVERLOAD: tracks.csv not found. Insert data to initiate protocol.")
