Night City Radio Analytics: Music DNA DashboardAn interactive data analytics dashboard built with Python and Streamlit for BAN-461: Advanced Data Modeling Systems.Analytical Question: Which musical characteristics (Energy, Danceability, Acousticness) define the most popular tracks, and how do these trends vary across different genres?Live App: [Paste your Streamlit Community Cloud URL here]GitHub Repo: [Paste your GitHub repository URL here]Project StructurePlaintext├── app.py               # Main Streamlit application with custom CSS
├── requirements.txt     # Python dependencies
├── tracks.csv           # Dataset (Music features and popularity scores)
└── README.md            # This file
Dashboard Features4 KPI metrics — Track Count, Avg Popularity, Sync (Danceability), and Chrome (Energy), all updating dynamically via the "Netrunner" interface.4 sidebar filters — Broadcast Station (Stylized select), User Alias, Genre Selection, and Energy Pulse Range.3 visualizations — Kinetic Sync (Scatter plot), Power Distribution (Grouped bar chart), and Waveform Trend (Linear analytics).Mission Briefing section — Analytical conclusions and Key Findings tied to the core musical research question.Archive Data Stream — Raw data view reflected through a themed high-contrast table.Encrypted Export — Ability to download the filtered dataset as a CSV for external analysis.Running LocallyPrerequisitesPython 3.9 or higherpipSetupClone the repositoryBashgit clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Create and activate a virtual environment (recommended)Bashpython -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
Install dependenciesBashpip install -r requirements.txt
Run the appBashstreamlit run app.py
DatasetThe dataset consists of various tracks and their corresponding audio features used to identify "hit" profiles. Key fields used in this dashboard:ColumnDescriptionTrack NameThe title of the song/audio nodeGenreMusical category used for meaningful dimension filteringPopularity0–100 score based on streaming volume and frequencyDanceabilityHow suitable a track is for dancing based on tempo and rhythmEnergyPerceptual measure of intensity and activityAcousticnessA confidence measure of whether the track is acousticLivenessDetects the presence of an audience in the recordingDependenciesPackagePurposestreamlitWeb app framework with custom CSS injection for the Cyberpunk UIpandasData cleaning and standardization of music metadataplotlyInteractive charts for visualizing musical characteristic correlationsnumpySupporting numerical operations for data normalization
