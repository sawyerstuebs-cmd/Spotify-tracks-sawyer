NIGHT CITY // AUDIO ANALYTICS DASHBOARD (Part 2)

An interactive cyberpunk-themed analytics dashboard built with Python and Streamlit for BAN‑461: Advanced Data Modeling Systems.

Analytical Question:
Which musical characteristics (Energy, Danceability, Acousticness) define the most popular tracks — and how do these trends vary across different genres?

Live App: (insert your Streamlit Community Cloud URL)
GitHub Repo: (insert your repository URL)

Project Structure:
app.py – Main Streamlit application
tracks.csv – Dataset used for analysis
requirements.txt – Python dependencies
README.txt – This file

Dashboard Features:
4 KPI Metrics: Sample Size, Avg Popularity, Avg Danceability, Avg Energy
2 Sidebar Filters: Genre selection and Energy range slider
3 Core Components: Mission Briefing, Scatter Plot, Genre Variance Bar Chart
Raw Data Table reflecting all filters
Cyberpunk UI Theme using custom CSS

Running Locally:
Prerequisites: Python 3.9 or higher, pip

Setup Steps:
1. Clone the repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate (macOS/Linux)
venv\Scripts\activate (Windows)

3. Install dependencies
pip install -r requirements.txt

4. Run the app
streamlit run app.py

5. Open in your browser
http://localhost:8501

Dataset Description:
The dashboard uses a tracks.csv dataset containing musical attributes for audio tracks.

Key Fields:
popularity – Popularity score of the track
danceability – Suitability for dancing (0–1)
energy – Intensity and activity level (0–1)
acousticness – Likelihood the track is acoustic (0–1)
genre – Genre label used for filtering
Other columns vary depending on dataset

If required columns are missing, the app automatically generates fallback values.

Dependencies:
streamlit – Web app framework
pandas – Data loading and transformation
plotly – Interactive visualizations
openpyxl – Excel file support if needed

Code Summary:
The dashboard includes a custom cyberpunk theme using injected CSS, a data engine that loads and cleans the tracks dataset, sidebar filters for genre and energy range, a Mission Briefing expander containing the analytical question and key findings, two visualizations answering the analytical question, and a raw data table for exploration.
