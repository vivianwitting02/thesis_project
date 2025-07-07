# Paying for Popularity: The Value of Online Attention in Soccer

This repository contains all files and notebooks used for my MSc AI thesis project, which investigates how online popularity relates to the market values of professional soccer players.

**The repository contains:**


**analysis/**

Contains core notebooks:

- EDA.ipynb: Exploratory Data Analysis of the dataset.
- modeling.ipynb: Contains the full model pipeline using regression and machine learning (OLS, Ridge, Random Forest, XGBoost, CatBoost, etc.).
- LSTM.ipynb: Experimented with LSTM, but not used in final thesis

**brandwatch/**

Includes all social media and news popularity metrics (mentions and sentiment) retrieved via Brandwatch for all players.

**dataframes/**

Cleaned and preprocessed datasets ready for modeling. Includes player-level and time-series versions.
- All_200_players contains all separate data from different sources
- final_versions contain the merged dataframes. The final versions used for analysis are: daily_final, monthly_final, and static_combined.csv

**mergers/**
Scripts and intermediate files used to merge all sources (player characteristics, performance data, and popularity metrics) into datasets.

**scrapers/**
Python scripts to scrape:
- Market value data from FootballTransfers
- Performance and characteristic data from WhoScored
