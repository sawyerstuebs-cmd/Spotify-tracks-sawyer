Spotify Artist Analytics DashboardAn interactive data analytics dashboard built with Python and Streamlit for BAN-461: Advanced Data Modeling Systems.Analytical Question: How does an artist's follower count impact their popularity score across different genres, and who are the top performers within the current market?Live App: (paste your Streamlit Community Cloud URL here) GitHub Repo: (paste your GitHub repository URL here)Project StructurePlaintext├── app.py               # Main Streamlit application
├── requirements.txt     # Python dependencies
├── artists.csv          # Dataset (Spotify artist metrics and genres)
└── README.md            # This file
Dashboard Features3 KPI metrics — Artists in View, Avg Popularity, and Max Followers, all updating dynamically with filters3 sidebar filters — User Name identification, Genre selection, and Popularity Score Range2 visualizations — Log-scaled scatter plot (Followers vs. Popularity) and a horizontal bar chart of Top Artists by FollowersKey Findings section — Analytical conclusions regarding viral success vs. legacy follower basesFiltered data table — Raw data view that reflects active filtersCSV export — Download the filtered artist list with one clickRunning LocallyPrerequisitesPython 3.9 or higherpipSetupClone the repositoryBashgit clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Create and activate a virtual environment (recommended)Bashpython -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
Install dependenciesBashpip install -r requirements.txt
Run the appBashstreamlit run app.py
Open in your browserStreamlit will automatically open the app. If it doesn't, navigate to:http://localhost:8501
DatasetThe dataset used in this dashboard contains metadata for thousands of Spotify artists. Key fields used in this dashboard:ColumnDescriptionnameThe name of the artistgenresMusical genres associated with the artistfollowersTotal number of Spotify followerspopularityA score (0-100) based on the artist's total playsDependenciesPackagePurposestreamlitWeb app frameworkpandasData loading and transformationplotlyInteractive charts and visualizations
