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
                color: #00FFFF; /* Standard Neon Cyan */
                font-family: 'Share Tech Mono', monospace;
            }

            /* Unified Glass Panels */
            [data-testid="stMetric"], .stPlotlyChart, .stDataFrame {
                background: rgba(10, 10, 10, 0.95) !important;
                border: 2px solid #FF00FF !important; /* Hot Pink Neon */
                border-radius: 0px !important;
                box-shadow: 0 0 15px rgba(255, 0, 255, 0.3);
            }

            /* Sidebar Overhaul */
            [data-testid="stSidebar"] {
                background-color: #000000 !important;
                border-right: 2px solid #00FFFF;
            }
            
            /* Text & Headers */
            h1, h2, h3 {
                font-family: 'Orbitron', sans-serif !important;
                color: #FF00FF !important;
                text-shadow: 0 0 10px #FF00FF;
                text-transform: uppercase;
            }

            /* Metric Styling */
            [data-testid="stMetricValue"] {
                color: #00FF66 !important;
                text-shadow: 0 0 10px #00FF66;
                font-size: 2.5rem !important;
            }

            /* Animations */
            @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
            .radio-active { animation: pulse 1s infinite; color: #00FF66; font-weight: bold; }
            
            @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
            .radio-disc { width: 80px; animation: spin 4s linear infinite; filter: drop-shadow(0 0 10px #00FFFF); }
        </style>
    """, unsafe_allow_html=True)

# --- 2. UI COMPONENTS ---
def render_radio_header(station_name, user_id):
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; 
                    background: #000; padding: 20px; border-bottom: 4px solid #00FFFF; margin-bottom: 25px;">
            <div style="display: flex; align-items: center; gap: 20px;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" class="radio-disc">
                <div>
                    <h1 style="margin:0;">{station_name}</h1>
                    <p class="radio-active">● SIGNAL_STRENGTH: MAXIMUM</p>
                </div>
            </div>
            <div style="text-align: right;">
                <p style="margin:0; color:#FF00FF;">NETRUNNER_AUTH: {user_id}</p>
                <p style="margin:0; font-size: 0.8rem; color:#666;">LOCATION: WATSON_DISTRICT</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- 3. DATA & LOGIC ---
@st.cache_data
def load_tracks():
    try:
        df = pd.read_csv("tracks.csv")
        df.columns = df.columns.str.strip().lower().str.replace(" ", "_")
        return df
    except:
        return pd.DataFrame()

# --- 4. MAIN APP ---
apply_night_city_theme()
df_raw = load_tracks()

if not df_raw.empty:
    name_col = 'track_name' if 'track_name' in df_raw.columns else df_raw.columns[1]

    # Sidebar 
    st.sidebar.markdown("### RADIO_CONTROL")
    station = st.sidebar.selectbox("STATION_SELECT", ["MORRO_ROCK_107.3", "BODY_HEAT_RADIO", "PEBBLE_DASH"])
    pilot = st.sidebar.text_input("USER_ALIAS", "V_001")
    
    # Filter Logic
    all_songs = sorted(df_raw[name_col].unique().astype(str))
    selected = st.sidebar.multiselect("QUEUE_TRACKS", all_songs, default=all_songs[:3])
    df = df_raw[df_raw[name_col].isin(selected)]

    # Layout
    render_radio_header(station, pilot)

    # Analytics Row
    st.markdown("### 📻 FREQUENCY_READOUT")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("TRACK_COUNT", len(df))
    col2.metric("HYPED_INDEX", f"{df['popularity'].mean():.1f}")
    col3.metric("BPM_SYNC", f"{df['danceability'].mean()*100:.0f}%")
    col4.metric("CHROME_LEVEL", f"{df['energy'].mean()*100:.0f}%")

    # Visualizer Row
    st.divider()
    v1, v2 = st.columns(2)
    
    # Unified Plotly Theme
    plotly_config = {
        'template': "plotly_dark",
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font_color': "#00FFFF"
    }

    with v1:
        st.markdown("### SIGNAL_POSITIONING")
        fig1 = px.scatter(df, x="danceability", y="popularity", color=name_col,
                         color_discrete_sequence=["#FF00FF", "#00FFFF", "#00FF66", "#FFCC00"])
        fig1.update_layout(**plotly_config)
        st.plotly_chart(fig1, use_container_width=True)

    with v2:
        st.markdown("### WAVEFORM_DISTORTION")
        fig2 = px.bar(df, x=name_col, y=["energy", "danceability"], barmode="group",
                     color_discrete_sequence=["#FF00FF", "#00FFFF"])
        fig2.update_layout(**plotly_config, xaxis={'tickangle': -45})
        st.plotly_chart(fig2, use_container_width=True)

    # Archive
    st.markdown("### ENCRYPTED_PLAYLIST_DATA")
    st.dataframe(df, use_container_width=True)
    
    st.markdown("<p style='text-align:center; color:#666; margin-top:40px;'>Good morning, Night City! Yesterday's body count rounded out to a solid and sturdy thirty!</p>", unsafe_allow_html=True)

else:
    st.error("FATAL_ERROR: tracks.csv not found in local deck.")
