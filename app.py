import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page config
st.set_page_config(page_title="Dragon Ball Spotify Analytics", page_icon="🐉", layout="wide")

# 2. Cyber-Saiyan CSS
st.markdown("""
    <style>
        /* Main Scouter Background */
        .stApp {
            background-color: #060b13;
            color: #ffffff;
            font-family: 'monospace';
        }
        
        /* Sidebar styling - Capsule Corp Gray */
        [data-testid="stSidebar"] {
            background-color: #1c252e;
            border-right: 2px solid #FF6600;
        }
        
        /* Scouter Section Headers */
        .section-header {
            font-size: 1.2rem;
            font-weight: 800;
            color: #FFCC00; /* Nimbus Yellow */
            text-transform: uppercase;
            letter-spacing: 3px;
            border-left: 5px solid #FF6600; /* Saiyan Orange */
            padding-left: 10px;
            margin-bottom: 15px;
            text-shadow: 2px 2px #cc5200;
        }

        /* Power Level (Metric) Styling */
        [data-testid="stMetricValue"] {
            color: #00FF00 !important; /* Scouter Green */
            font-family: 'DotGothic16', monospace;
            text-shadow: 0 0 5px #00FF00;
        }
        
        /* Button & UI Glow */
        .stButton>button {
            background-color: #FF6600;
            color: white;
            border-radius: 20px;
            border: 2px solid #FFCC00;
            box-shadow: 0 0 10px #FF6600;
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
        st.error(f"SYSTEM ERROR: Dragon Balls Scattered: {e}")
        return pd.DataFrame()

df_raw = load_data()

# 4. Filter logic
if not df_raw.empty:
    genre_col = 'track_genre' if 'track_genre' in df_raw.columns else df_raw.columns[0]

    # Sidebar
    st.sidebar.markdown("<h2 style='color:#FF6600;'>CAPSULE_CORP_UI</h2>", unsafe_allow_html=True)
    user_name = st.sidebar.text_input("SCANNING BIOMETRICS (Name):", placeholder="Goku / Vegeta")

    all_genres = sorted(df_raw[genre_col].unique().astype(str))
    selected_genres = st.sidebar.multiselect("GENRE_SAGA", options=all_genres, default=all_genres[0:3])
    pop_range = st.sidebar.slider("POWER_LEVEL_LIMIT", 0, 100, (40, 100))

    # Apply filters
    df = df_raw[df_raw[genre_col].isin(selected_genres)]
    df = df[df["popularity"].between(pop_range[0], pop_range[1])]

    # 5. Header
    st.markdown("<h1 style='color: #FF6600; text-align: center; text-shadow: 3px 3px #FFCC00;'>🎵 KAMI'S SPOTIFY LOOKOUT</h1>", unsafe_allow_html=True)
    
    if user_name:
        st.markdown(f"<p style='text-align: center; color: #00FF00;'>SENSING KI ENERGY FROM: <b>{user_name.upper()}</b></p>", unsafe_allow_html=True)
    
    st.markdown("<p style='text-align: center; font-style: italic; color: #888;'>'I am the hope of the universe. I am the answer to all music who cry out for peace!'</p>", unsafe_allow_html=True)
    st.divider()

    # 6. Scouter KPIs
    st.markdown('<p class="section-header">SCOUTER_DATA_READOUT</p>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("TRACK_ENTITIES", f"{len(df):,}")
    k2.metric("AVG_POWER_LVL", f"{df['popularity'].mean():.1f}" if not df.empty else "0")
    k3.metric("RHYTHMIC_KI", f"{df['danceability'].mean()*100:.1f}%" if 'danceability' in df.columns else "0%")
    k4.metric("ENERGY_STAMINA", f"{df['energy'].mean()*100:.1f}%" if 'energy' in df.columns else "0%")

    # 7. Saiyan Visualizations
    st.divider()
    col1, col2 = st.columns(2)

    # Dragon Ball Color Palette (Orange, Yellow, Blue, Red, Green)
    dbz_colors = ["#FF6600", "#FFCC00", "#2E86AB", "#FF0000", "#00FF00"]

    with col1:
        if 'danceability' in df.columns:
            fig1 = px.scatter(df, x="danceability", y="popularity", color=genre_col, 
                             title="COMBAT_CORRELATION: DANCE vs POWER",
                             color_discrete_sequence=dbz_colors)
            fig1.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig1, use_container_width=True)

    with col2:
        if 'energy' in df.columns:
            feat_means = df.groupby(genre_col)[["energy", "danceability"]].mean().reset_index()
            fig2 = px.bar(feat_means, x=genre_col, y=["energy", "danceability"], barmode="group",
                         title="FORMS_SPECTRUM: ENERGY/DANCE", 
                         color_discrete_sequence=["#FF6600", "#2E86AB"])
            fig2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig2, use_container_width=True)

    # 8. Raw Data Table
    st.divider()
    st.markdown('<p class="section-header">Z-FIGHTER_RECORDS</p>', unsafe_allow_html=True)
    st.dataframe(df.head(50).style.set_properties(**{'background-color': '#1c252e', 'color': '#FFCC00', 'border-color': '#FF6600'}))
else:
    st.error("IT'S OVER 9000 (errors)! Check your tracks.csv file path.")
