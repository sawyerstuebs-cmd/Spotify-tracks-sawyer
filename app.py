import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page config
st.set_page_config(page_title="FATAL ANALYTICS", page_icon="🐉", layout="wide")

# 2. Hybrid Aesthetic CSS (Contrasting Fonts + MK Animations)
st.markdown("""
    <style>
        /* Fonts: Importing Google Fonts for contrast */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Share+Tech+Mono&display=swap');

        .stApp {
            background-color: #0a0e14;
            color: #ffffff;
        }

        /* Header Font: Aggressive Orbitron */
        h1, h2, .section-header {
            font-family: 'Orbitron', sans-serif !important;
            letter-spacing: 3px;
        }

        /* Body Font: Tech Mono for Readability */
        p, span, label, .stMetric {
            font-family: 'Share Tech Mono', monospace !important;
        }

        /* Section Headers with NERV/MK Blood Red/Purple contrast */
        .section-header {
            font-size: 1.2rem;
            color: #FF0033; /* Blood Red */
            background: rgba(160, 101, 212, 0.1); /* Faint Eva Purple */
            padding: 8px;
            border-left: 5px solid #FF6600; /* Saiyan Orange */
            border-right: 5px solid #FF0033;
            text-align: center;
            text-shadow: 2px 2px #000000;
        }

        /* Mortal Kombat Character Positioning */
        .character-container {
            display: flex;
            justify-content: space-between;
            padding: 0 50px;
            margin-bottom: -50px;
        }

        .mk-sprite {
            height: 150px;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Moving Mortal Kombat Characters (Visual Overlay)
# Using classic GIFs of Scorpion and Sub-Zero
st.markdown("""
    <div class="character-container">
        <img src="https://www.fightersgeneration.com/characters4/scorpion-classic-stance.gif" class="mk-sprite">
        <img src="https://www.fightersgeneration.com/characters4/subzero-classic-stance.gif" class="mk-sprite">
    </div>
""", unsafe_allow_html=True)

# 4. Data loading
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("tracks.csv")
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        return df
    except Exception as e:
        st.error(f"FATALITY: Data Link Severed: {e}")
        return pd.DataFrame()

df_raw = load_data()

# 5. Filter logic
if not df_raw.empty:
    genre_col = 'track_genre' if 'track_genre' in df_raw.columns else df_raw.columns[0]

    st.sidebar.markdown("<h1 style='color:#FF0033; font-family:Orbitron;'>KOMBAT_MENU</h1>", unsafe_allow_html=True)
    user_name = st.sidebar.text_input("ENTER KOMBATANT NAME:", placeholder="Scorpion / Shinji")

    all_genres = sorted(df_raw[genre_col].unique().astype(str))
    selected_genres = st.sidebar.multiselect("CHOOSE REALM (GENRE):", options=all_genres, default=all_genres[0:3])
    pop_range = st.sidebar.slider("SYNC_LEVEL", 0, 100, (40, 100))

    # Apply filters
    df = df_raw[df_raw[genre_col].isin(selected_genres)]
    df = df[df["popularity"].between(pop_range[0], pop_range[1])]

    # 6. Header
    st.markdown("<h1 style='color: #FFCC00; text-align: center; font-size: 3.5rem; text-shadow: 4px 4px #FF0033;'>TEST YOUR MIGHT</h1>", unsafe_allow_html=True)
    
    if user_name:
        st.markdown(f"<p style='text-align: center; color: #00FF99; font-size: 1.5rem;'>FIGHTER: {user_name.upper()}</p>", unsafe_allow_html=True)
    
    st.divider()

    # 7. Metrics (KPIs)
    st.markdown('<p class="section-header">BATTLE_STATS</p>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("NODES_CONQUERED", f"{len(df):,}")
    k2.metric("POWER_RATING", f"{df['popularity'].mean():.1f}" if not df.empty else "0")
    k3.metric("AGILITY (DANCE)", f"{df['danceability'].mean()*100:.1f}%" if 'danceability' in df.columns else "0%")
    k4.metric("STAMINA (ENERGY)", f"{df['energy'].mean()*100:.1f}%" if 'energy' in df.columns else "0%")

    # 8. Visualizations
    st.divider()
    col1, col2 = st.columns(2)

    # High Contrast Colors: Scorpion Yellow, Sub-Zero Blue, Eva Purple, Blood Red
    mk_palette = ["#FFCC00", "#00CCFF", "#A065D4", "#FF0033", "#00FF99"]

    with col1:
        if 'danceability' in df.columns:
            fig1 = px.scatter(df, x="danceability", y="popularity", color=genre_col, 
                             title="COMBAT_CORRELATION",
                             color_discrete_sequence=mk_palette)
            fig1.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', 
                              plot_bgcolor='rgba(255,255,255,0.05)')
            st.plotly_chart(fig1, use_container_width=True)

    with col2:
        if 'energy' in df.columns:
            feat_means = df.groupby(genre_col)[["energy", "danceability"]].mean().reset_index()
            fig2 = px.bar(feat_means, x=genre_col, y=["energy", "danceability"], barmode="group",
                         title="REALM_ANALYSIS", 
                         color_discrete_sequence=["#FF0033", "#00CCFF"])
            fig2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', 
                              plot_bgcolor='rgba(255,255,255,0.05)')
            st.plotly_chart(fig2, use_container_width=True)

    # 9. Data Table
    st.divider()
    st.markdown('<p class="section-header">KRYPT_ARCHIVES</p>', unsafe_allow_html=True)
    st.dataframe(df.head(50), use_container_width=True)
    
    st.sidebar.markdown("---")
    if st.sidebar.button("FINISH HIM (Reset)"):
        st.rerun()
else:
    st.error("ROUND 1: FAILED. Check tracks.csv.")
