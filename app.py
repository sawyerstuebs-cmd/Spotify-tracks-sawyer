import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. CORE THEME & CSS ---
st.set_page_config(page_title="NIGHT CITY RADIO", page_icon="📻", layout="wide")

def apply_night_city_theme():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Share+Tech+Mono&display=swap');

            /* Global Styles */
            .stApp {
                background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                            url('https://images.unsplash.com/photo-1605806616949-1e87b487fc2f?q=80&w=2000');
                background-size: cover;
                background-attachment: fixed;
                color: #00FFFF; 
                font-family: 'Share Tech Mono', monospace;
            }

            /* Unified Glass Panels */
            [data-testid="stMetric"], .stPlotlyChart, .stDataFrame, .stTable {
                background: rgba(0, 0, 0, 0.95) !important;
                border: 2px solid #FF00FF !important; 
                border-radius: 0px !important;
                padding: 10px;
            }

            /* Sidebar Overhaul */
            [data-testid="stSidebar"] {
                background-color: #000000 !important;
                border-right: 2px solid #00FFFF;
            }
            
            /* Typography */
            h1, h2, h3, label, p {
                font-family: 'Orbitron', sans-serif !important;
                text-transform: uppercase;
            }
            
            h1, h2, h3 {
                color: #FF00FF !important;
                text-shadow: 0 0 10px #FF00FF;
            }

            /* Metric Styling */
            [data-testid="stMetricValue"] {
                color: #00FF66 !important;
                text-shadow: 0 0 10px #00FF66;
                font-size: 2.5rem !important;
            }

            /* Animations */
            @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
            .radio-disc { width: 80px; animation: spin 4s linear infinite; filter: drop-shadow(0 0 10px #00FFFF); }
            
            .status-glow { color: #00FF66; animation: pulse 2s infinite; font-weight: bold; }
            @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
        </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ENGINE (The "Fix") ---
@st.cache_data
def load_tracks():
    try:
        # Attempt to load the CSV
        df = pd.read_csv("tracks.csv")
        # Clean column names (strip whitespace, lowercase, underscores)
        df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
        
        # Ensure numerical columns exist or create dummy data for visualization
        cols = df.columns
        if 'popularity' not in cols: df['popularity'] = 50
        if 'danceability' not in cols: df['danceability'] = 0.5
        if 'energy' not in cols: df['energy'] = 0.5
        
        return df
    except FileNotFoundError:
        # If file is missing, create a small sample so the app doesn't crash
        st.error("⚠️ DATA LINK SEVERED: 'tracks.csv' not found. Loading emergency buffer...")
        data = {
            'track_name': ['Resist and Disorder', 'Never Fade Away', 'Chippin In'],
            'popularity': [90, 95, 85],
            'danceability': [0.7, 0.6, 0.8],
            'energy': [0.9, 0.8, 0.95]
        }
        return pd.DataFrame(data)

# --- 3. UI COMPONENTS ---
def render_header(station, pilot):
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; 
                    background: #000; padding: 20px; border-bottom: 4px solid #00FFFF; margin-bottom: 25px;">
            <div style="display: flex; align-items: center; gap: 20px;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" class="radio-disc">
                <div>
                    <h1 style="margin:0;">{station}</h1>
                    <p class="status-glow">● SIGNAL_STRENGTH: OPTIMAL</p>
                </div>
            </div>
            <div style="text-align: right;">
                <p style="margin:0; color:#FF00FF;">ID: {pilot}</p>
                <p style="margin:0; font-size: 0.7rem; color:#666;">GRID_LOC: NC_WATSON_01</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- 4. MAIN APP ---
apply_night_city_theme()
df_raw = load_tracks()

if not df_raw.empty:
    # Dynamically find the name column
    name_col = 'track_name' if 'track_name' in df_raw.columns else df_raw.columns[0]

    # Sidebar 
    st.sidebar.markdown("### RADIO_DECK_v1")
    station_choice = st.sidebar.selectbox("FREQ_SELECT", ["MORRO_ROCK_107.3", "BODY_HEAT", "VEXELSTROM"])
    pilot_alias = st.sidebar.text_input("NETRUNNER_ALIAS", "V")
    
    # Filter Logic
    all_songs = sorted(df_raw[name_col].unique().astype(str))
    selected = st.sidebar.multiselect("QUEUE_ENCRYPTION", all_songs, default=all_songs[:3] if len(all_songs) >= 3 else all_songs)
    
    df_filtered = df_raw[df_raw[name_col].isin(selected)]

    # Header
    render_header(station_choice, pilot_alias)

    # Analytics
    st.markdown("### 📊 SIGNAL_METRICS")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("TRACKS", len(df_filtered))
    m2.metric("HYPED", f"{df_filtered['popularity'].mean():.1f}")
    m3.metric("SYNC", f"{df_filtered['danceability'].mean()*100:.0f}%")
    m4.metric("KI_ENERGY", f"{df_filtered['energy'].mean()*100:.0f}%")

    # Visuals
    st.divider()
    v1, v2 = st.columns(2)
    
    chart_style = {
        'template': "plotly_dark",
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font_color': "#00FFFF"
    }

    with v1:
        st.markdown("### KINETIC_WAVEFORM")
        fig1 = px.scatter(df_filtered, x="danceability", y="popularity", color=name_col,
                         color_discrete_sequence=["#FF00FF", "#00FFFF", "#00FF66"])
        fig1.update_layout(**chart_style)
        st.plotly_chart(fig1, use_container_width=True)

    with v2:
        st.markdown("### POWER_DISTRIBUTION")
        fig2 = px.bar(df_filtered, x=name_col, y=["energy", "danceability"], barmode="group",
                     color_discrete_sequence=["#FF00FF", "#00FFFF"])
        fig2.update_layout(**chart_style)
        st.plotly_chart(fig2, use_container_width=True)

    # Data Archive
    st.markdown("### 📂 ARCHIVE_LOGS")
    st.dataframe(df_filtered, use_container_width=True)
    
    st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>'Wrong city, wrong people.' — Johnny Silverhand</p>", unsafe_allow_html=True)
