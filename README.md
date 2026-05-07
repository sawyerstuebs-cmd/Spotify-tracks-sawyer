# Night City Radio: Music DNA Analytics Dashboard

An interactive data analytics dashboard built with Python and Streamlit for **BAN-461: Advanced Data Modeling Systems**.

**Analytical Question:** *Which musical characteristics (Energy, Danceability, Acousticness) define the most popular tracks, and how do these trends vary across different genres?*

**Live App:** *(paste your Streamlit Community Cloud URL here)*
**GitHub Repo:** *(paste your GitHub repository URL here)*

---

## Project Structure

```text
├── app.py               # Main Streamlit application
├── requirements.txt     # Python dependencies
├── tracks.csv           # Dataset (Audio features & popularity scores)
└── README.md            # This file
Dashboard Features4 KPI metrics — Track Nodes, Avg Popularity, Sync (Danceability), and Chrome (Energy), all updating dynamically with filters4 sidebar filters — Radio Station, Netrunner ID, Genre Dimension, and Energy Pulse Range3 visualizations — Kinetic Sync scatter plot, Power Distribution bar chart, and Data Waveform popularity trendMission Briefing section — Analytical conclusions tied to music trend discoveryArchive Data Stream — Raw data view that reflects active netrunner filtersCSV export — Download the filtered dataset with one clickRunning LocallyPrerequisitesPython 3.9 or higherpipSetupClone the repositoryBashgit clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
Create and activate a virtual environment (recommended)Bashpython -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
Install dependenciesBashpip install -r requirements.txt
Run the appBashstreamlit run app.py
DatasetKey fields used in this dashboard:ColumnDescriptiontrack_nameThe title of the song/audio nodegenreMusical category used for meaningful dimension filteringpopularity0–100 score based on streaming volume and frequencydanceabilitySuitability for dancing based on tempo and rhythm stabilityenergyPerceptual measure of intensity, activity, and dynamic rangeacousticnessConfidence measure of whether the track is acousticvalenceMeasure of the musical positiveness conveyed by a trackDependenciesPackagePurposestreamlitWeb app frameworkpandasData loading and transformationplotlyInteractive chartsnumpySupporting numerical operations
