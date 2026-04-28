import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page config
st.set_page_config(page_title="NERV Scouter Analytics", page_icon="🤖", layout="wide")

# 2. Hybrid Aesthetic CSS (NGE Purple + Saiyan Orange + Cyberpunk Neon)
st.markdown("""
    <style>
        /* Tactical Slate Background - easier on the eyes than pure black */
        .stApp {
            background-color: #1a1c2c;
            color: #e0e0e0;
            font-family: 'Share Tech Mono', monospace;
        }
        
        /* Sidebar - NERV Command Center Style */
        [data-testid="stSidebar"] {
            background-color: #0f111a;
            border-right: 3px solid #A065D4; /* Eva-01 Purple */
        }
        
        /* Section Headers - Emergency Protocol Style */
        .section-header {
            font-size: 1.1rem;
            font-weight: 800;
            color: #FFCC00; /* LCL Yellow */
            background: linear-gradient(90deg, #FF6600, transparent); /* Saiyan Orange */
            padding: 5px 15px;
            border-left: 5px solid #A065D4;
            letter-spacing: 2px;
            margin-bottom: 20px;
        }

        /* Power Level (Metric) Styling - Scouter Green */
        [data-testid="stMetricValue"] {
            color: #00FF99 !important; 
            text-shadow: 0 0 10px #00FF99;
        }
        
        /* Dataframe Styling */
        .stDataFrame {
            border: 1px solid #A065D4;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Data loading
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("tracks.csv")
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        return df
    except Exception as e:
        st.error(f"SYSTEM ERROR: 3rd Impact Imminent: {e}")
        return pd.DataFrame()

df_raw = load_data()

# 4. Filter logic
if not df_raw.empty:
    genre_col = 'track_genre' if 'track_genre' in df_raw.columns else df_raw.columns[0]

    st.sidebar.markdown("<h2 style='color:#A065D4;'>NERV_INTERFACE</h2>", unsafe_allow_html=True)
    user_name = st.sidebar.text_input("IDENTIFY PILOT:", placeholder="Shinji / Vegeta")

    all_genres = sorted(df_raw[genre_col].unique().astype(str))
    selected_genres = st.sidebar.multiselect("SELECT_SAGA_GENRE", options=all_genres, default=all_genres[0:3])
    pop_range = st.sidebar.slider("SYNC_RATIO_POWER", 0, 100, (40, 100))

    # Apply filters
    df = df_raw[df_raw[genre_col].isin(selected_genres)]
    df = df[df["popularity"].between(pop_range[0], pop_range[1])]

    # 5. Header
    st.markdown("<h1 style='color: #FF6600; text-align: center; text-shadow: 2px 2px #A065D4;'>EVA-SAIYAN ANALYTICS GRID</h1>", unsafe_allow_html=True)
    
    if user_name:
        st.markdown(f"<p style='text-align: center; color: #00FF99;'>PILOT SYNCHRONIZATION: <b>{user_name.upper()} - 100%</b></p>", unsafe_allow_html=True)
    
    st.markdown("<p style='text-align: center; font-size: 0.8rem; color: #888;'>'Pattern Blue Detected. Energy levels rising above 9,000...'</p>", unsafe_allow_html=True)
    st.divider()

    # 6. Metrics (KPIs)
    st.markdown('<p class="section-header">TACTICAL_READOUT</p>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("NODES_IN_VIEW", f"{len(df):,}")
    k2.metric("POWER_LEVEL", f"{df['popularity'].mean():.1f}" if not df.empty else "0")
    k3.metric("SYNC_RATE (DANCE)", f"{df['danceability'].mean()*100:.1f}%" if 'danceability' in df.columns else "0%")
    k4.metric("AT_FIELD_STRENGTH", f"{df['energy'].mean()*100:.1f}%" if 'energy' in df.columns else "0%")

    # 7. Visualizations
    st.divider()
    col1, col2 = st.columns(2)

    # Hybrid Palette: Eva Purple, Saiyan Orange, Cyan, LCL Yellow
    hybrid_colors = ["#A065D4", "#FF6600", "#00FFFF", "#FFCC00", "#FF0055"]

    with col1:
        if 'danceability' in df.columns:
            fig1 = px.scatter(df, x="danceability", y="popularity", color=genre_col, 
                             title="SYNC vs POWER SCATTER",
                             color_discrete_sequence=hybrid_colors)
            # Layout adjustment for readability
            fig1.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', 
                              plot_bgcolor='rgba(255,255,255,0.05)') # Slight tint for grid visibility
            st.plotly_chart(fig1, use_container_width=True)

    with col2:
        if 'energy' in df.columns:
            feat_means = df.groupby(genre_col)[["energy", "danceability"]].mean().reset_index()
            fig2 = px.bar(feat_means, x=genre_col, y=["energy", "danceability"], barmode="group",
                         title="GENRE_WAVEFORM_ANALYSIS", 
                         color_discrete_sequence=["#A065D4", "#FF6600"])
            fig2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', 
                              plot_bgcolor='rgba(255,255,255,0.05)')
            st.plotly_chart(fig2, use_container_width=True)

    # 8. Data Table
    st.divider()
    st.markdown('<p class="section-header">NERV_ARCHIVE_LOGS</p>', unsafe_allow_html=True)
    # Slate background for the table makes text much easier to read
    st.dataframe(df.head(50), use_container_width=True)
else:
    st.error("ERROR: MAGI System Offline. Upload tracks.csv immediately.")
