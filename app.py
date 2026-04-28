import streamlit as st
import pandas as pd
import plotly.express as px
import html
from pathlib import Path

# --- 1. CORE THEME & CSS ---
st.set_page_config(page_title="NIGHT CITY RADIO", page_icon="📻", layout="wide")

def apply_night_city_theme():
    """Applies the Cyberpunk visual layer via CSS injection."""
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Share+Tech+Mono&display=swap');

            .stApp {
                background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                            url('https://images.unsplash.com/photo-1605806616949-1e87b487fc2f?q=80&w=2000');
                background-size: cover;
                background-attachment: fixed;
                color: #00FFFF; 
                font-family: 'Share Tech Mono', monospace;
            }

            [data-testid="stMetric"], .stPlotlyChart, .stDataFrame {
                background: rgba(0, 0, 0, 0.95) !important;
                border: 2px solid #FF00FF !important; 
                box-shadow: 0 0 15px rgba(255, 0, 255, 0.2);
            }

            [data-testid="stSidebar"] {
                background-color: #000000 !important;
                border-right: 2px solid #00FFFF;
            }
            
            h1, h2, h3, label {
                font-family: 'Orbitron', sans-serif !important;
                text-transform: uppercase;
                color: #FF00FF !important;
                text-shadow: 0 0 8px #FF00FF;
            }

            [data-testid="stMetricValue"] {
                color: #00FF66 !important;
                text-shadow: 0 0 10px #00FF66;
            }

            @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
            .radio-disc { width: 70px; animation: spin 4s linear infinite; filter: drop-shadow(0 0 10px #00FFFF); }
            
            .status-glow { color: #00FF66; animation: pulse 2s infinite; font-weight: bold; font-size: 0.8rem; }
            @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
        </style>
    """, unsafe_allow_html=True)

# --- 2. SECURE DATA ENGINE ---
@st.cache_data
def load_tracks(file_path: str):
    """Loads and sanitizes the track database."""
    if not Path(file_path).is_file():
        return None

    try:
        df = pd.read_csv(file_path)
        # Standardize headers: lowercase, no spaces
        df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
        
        # Ensure critical columns exist to prevent downstream crashes
        required_cols = ['popularity', 'danceability', 'energy']
        for col in required_cols:
            if col not in df.columns:
                df[col] = 0.0
        
        return df
    except Exception as e:
        st.error(f"DATA_LINK_CORRUPTED: {e}")
        return None

# --- 3. UI COMPONENTS ---
def render_header(station, pilot):
    """Renders the top HUD with XSS protection."""
    # SECURITY: Escape user input to prevent HTML injection
    safe_station = html.escape(station)
    safe_pilot = html.escape(pilot)

    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; 
                    background: #000; padding: 20px; border-bottom: 4px solid #00FFFF; margin-bottom: 25px;">
            <div style="display: flex; align-items: center; gap: 20px;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" class="radio-disc">
                <div>
                    <h1 style="margin:0; font-size: 1.8rem;">{safe_station}</h1>
                    <p class="status-glow">● BROADCAST_LIVE // NIGHT_CITY_RADIO</p>
                </div>
            </div>
            <div style="text-align: right;">
                <p style="margin:0; color:#FF00FF; font-family: 'Orbitron';">USER: {safe_pilot}</p>
                <p style="margin:0; font-size: 0.7rem; color:#666;">DECK_VER: NC_SECURE_2.0</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- 4. MAIN APP ---
apply_night_city_theme()
df_raw = load_tracks("tracks.csv")

if df_raw is not None:
    # Identify the track title column dynamically
    name_options = ['track_name', 'name', 'track_title', 'title']
    title_col = next((col for col in name_options if col in df_raw.columns), df_raw.columns[0])

    # Sidebar Controls
    st.sidebar.markdown("### DECK_CONTROLS")
    station_choice = st.sidebar.selectbox("STATION", ["MORRO_ROCK_RADIO", "BODY_HEAT_NC", "VEXELSTROM"])
    pilot_alias = st.sidebar.text_input("NETRUNNER_ID", value="V", max_chars=20)
    
    all_titles = sorted(df_raw[title_col].unique().astype(str))
    selected_songs = st.sidebar.multiselect(
        "QUEUE_ENCRYPTION", 
        options=all_titles, 
        default=all_titles[:3] if len(all_titles) >= 3 else all_titles
    )
    
    # Filter and display
    df_filtered = df_raw[df_raw[title_col].isin(selected_songs)]
    render_header(station_choice, pilot_alias)

    if not df_filtered.empty:
        # Analytics HUD
        st.markdown("### 📊 SIGNAL_STRENGTH")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("TRACKS", len(df_filtered))
        m2.metric("HYPED", f"{df_filtered['popularity'].mean():.1f}")
        m3.metric("SYNC", f"{df_filtered['danceability'].mean()*100:.0f}%")
        m4.metric("CHROME", f"{df_filtered['energy'].mean()*100:.0f}%")

        # Visualizers
        st.divider()
        v1, v2 = st.columns(2)
        chart_theme = {'template': "plotly_dark", 'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)', 'font_color': "#00FFFF"}

        with v1:
            st.markdown("### KINETIC_SYNC")
            fig1 = px.scatter(df_filtered, x="danceability", y="popularity", color=title_col,
                             color_discrete_sequence=["#FF00FF", "#00FFFF", "#00FF66"])
            fig1.update_layout(**
