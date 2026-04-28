import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. SETTINGS & STYLES ---
st.set_page_config(page_title="SCIFI_OS_v2", page_icon="💊", layout="wide")

def apply_custom_styles():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Share+Tech+Mono&family=Vt323&display=swap');

            /* Clean Cyber-Rain Background */
            .stApp {
                background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                            url('https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?q=80&w=2000');
                background-size: cover;
                color: #ffffff;
                font-family: 'Share Tech Mono', monospace;
            }

            /* Modular Glass Panels */
            .glass-panel {
                background: rgba(0, 0, 0, 0.85);
                border: 1px solid #FF6600;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 4px 15px rgba(255, 102, 0, 0.2);
            }

            /* Sidebar: Bebop Blue x Arrakis Gold */
            [data-testid="stSidebar"] {
                background-color: #050510 !important;
                border-right: 2px solid #00FFFF;
            }

            /* Metrics: Scouter Green */
            [data-testid="stMetricValue"] {
                color: #00FF66 !important;
                text-shadow: 0 0 10px #00FF66;
                font-family: 'Vt323', monospace !important;
                font-size: 2.8rem !important;
            }

            /* Headers */
            .section-header {
                color: #FFCC00;
                border-left: 5px solid #FF6600;
                padding-left: 15px;
                font-family: 'Orbitron', sans-serif;
                font-size: 1.1rem;
                margin: 20px 0;
            }
            
            /* Animations */
            @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
            .vinyl { width: 60px; animation: spin 3s linear infinite; filter: drop-shadow(0 0 10px #FF0033); }
        </style>
    """, unsafe_allow_html=True)

# --- 2. COMPONENTS ---
def render_header(title):
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; 
                    background: #000; padding: 20px; border-bottom: 3px solid #FF0033; margin-bottom: 30px;">
            <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3NueXpqcXR3bmR3bmR3bmR3bmR3bmR3bmR3bmR3bmR3bmR3bmR3JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/4ilFRqgbzbx4c/giphy.gif" height="60">
            <h1 style="font-family: 'Orbitron'; margin: 0; color: #fff;">{title}</h1>
            <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" class="vinyl">
        </div>
    """, unsafe_allow_html=True)

# --- 3. DATA ENGINE ---
@st.cache_data
def get_data():
    try:
        df = pd.read_csv("tracks.csv")
        df.columns = df.columns.str.strip().lower().str.replace(" ", "_")
        return df
    except:
        return pd.DataFrame()

# --- 4. MAIN EXECUTION ---
apply_custom_styles()
df_raw = get_data()

if not df_raw.empty:
    name_col = 'track_name' if 'track_name' in df_raw.columns else df_raw.columns[1]

    # Sidebar UI
    st.sidebar.title("📡 NAVIGATION")
    pilot = st.sidebar.text_input("USER_ID", "KORBEN_DALLAS")
    track_list = sorted(df_raw[name_col].unique().astype(str))
    targets = st.sidebar.multiselect("TRACK_SELECTION", track_list, default=track_list[:3])
    
    df = df_raw[df_raw[name_col].isin(targets)]

    render_header(f"{pilot} // SYSTEM_OS")

    # Metrics Row
    st.markdown('<p class="section-header">VITAL_DATA_READOUT</p>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("NODES", len(df))
    m2.metric("POP", f"{df['popularity'].mean():.1f}")
    m3.metric("SYNC", f"{df['danceability'].mean()*100:.0f}%")
    m4.metric("KI", f"{df['energy'].mean()*100:.0f}%")

    # Visuals Row
    st.divider()
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown('<p class="section-header">KINETIC_TRACKING</p>', unsafe_allow_html=True)
        fig1 = px.scatter(df, x="danceability", y="popularity", color=name_col,
                         color_discrete_sequence=["#FF6600", "#00FFFF", "#FF00FF"])
        fig1.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        st.markdown('<p class="section-header">PULSE_ANALYSIS</p>', unsafe_allow_html=True)
        fig2 = px.bar(df, x=name_col, y=["energy", "danceability"], barmode="group",
                     color_discrete_sequence=["#FF0033", "#00FFFF"])
        fig2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)

    # Logs
    st.markdown('<p class="section-header">MULTIPASS_LOGS</p>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
    
    st.markdown("<p style='text-align:center; color:#FF6600; margin-top:50px;'>SEE YOU SPACE COWBOY...</p>", unsafe_allow_html=True)

else:
    st.error("SYSTEM ERROR: UNABLE TO ACCESS tracks.csv")
