"""
Created by: Vivian Witting
Date: 28/05/2025

* This file forward fills the performance data per match,
to prevent the data from containing too many nan values.
"""

import pandas as pd

# Load datasets 
monthly_df = pd.read_csv("../dataframes/final_versions/monthly_encoded.csv", sep="\t")
static_df = pd.read_csv("../dataframes/final_versions/static_dataset.csv", sep="\t")
daily_df = pd.read_csv("../dataframes/final_versions/daily_player_dataset.csv", sep="\t")

# Create national_team indicator from daily data
national_keywords = ["nations league", "world cup", "euro", "qualifier", "international friendly"]

def is_national_match(league):
    if pd.isna(league):
        return 0
    return int(any(k in league.lower() for k in national_keywords))

daily_df["national_team_match"] = daily_df["league"].apply(is_national_match)
national_team_flag = daily_df.groupby("player_id")["national_team_match"].max().reset_index()
national_team_flag.columns = ["player_id", "national_team"]

# Clean monthly data
cols_to_exclude = [
    "month", "current_team_enc",
    "total_mentions_lag2", "goals_per_match_lag1",
    "pass_success_avg_lag1", "rating_avg_lag1"
]
monthly_clean = monthly_df.drop(columns=[col for col in cols_to_exclude if col in monthly_df.columns])
monthly_clean = monthly_clean.select_dtypes(include=["number"])
monthly_avg = monthly_clean.groupby("player_id").mean().reset_index()

# Merge static + monthly averages 
static_merged = static_df.merge(monthly_avg, on="player_id", how="left")

# Merge national_team flag
static_merged = static_merged.merge(national_team_flag, on="player_id", how="left")
static_merged["national_team"] = static_merged["national_team"].fillna(0).astype(int)

# Drop _x columns (original static duplicates), keep others
static_merged = static_merged.drop(columns=[col for col in static_merged.columns if col.endswith('_x')])
static_merged.columns = [col.replace('_y', '') for col in static_merged.columns]

# Save final result
static_merged.to_csv("../dataframes/final_versions/static_combined.csv", sep="\t", index=False)
print("Static combined dataset saved to: static_combined.csv")
