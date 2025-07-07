"""
Created by: Vivian Witting
Date: 28/05/2025

* This file filters out players with less than 5 months of performance data
* Thereafter it ffill performance between the still empty months
* It also adds the total_mentions_lag1 with a shift of 1 month
"""

import pandas as pd
import numpy as np

performance_cols = [
    "mins_played_avg", "goals_per_match", "assists_per_match",
    "rating_avg", "shots_per_match", "aerials_won_per_match", "pass_success_avg"
]


def filter_players(df):
    df["performance_valid"] = df[performance_cols].notna().sum(axis=1)
    performance_counts = df.groupby("player_id")["performance_valid"].apply(lambda x: (x > 0).sum())

    valid_players = performance_counts[performance_counts >= 5].index
    df = df[df["player_id"].isin(valid_players)].copy()

    return df


def fill_performance(df):
    df.sort_values(["player_id", "month"], inplace=True)
    df[performance_cols] = df.groupby("player_id")[performance_cols].transform(lambda x: x.ffill().bfill())

    df["total_mentions_lag1"] = df.groupby("player_id")["total_mentions"].shift(1)
    df["total_mentions_lag2"] = df.groupby("player_id")["total_mentions"].shift(2)
    
    df["goals_per_match_lag1"] = df.groupby("player_id")["goals_per_match"].shift(1)
    df["pass_success_avg_lag1"] = df.groupby("player_id")["pass_success_avg"].shift(1)
    df["rating_avg_lag1"] = df.groupby("player_id")["rating_avg"].shift(1)

    df = df.dropna(subset=["total_mentions_lag1"])
    df.drop(columns=["performance_valid"], inplace=True)

    return df


def main():
    df = pd.read_csv("../dataframes/final_versions/monthly_player_dataset.csv", sep="\t")
    df = filter_players(df)
    df = fill_performance(df)

    df["log_market_value"] = np.log1p(df["market_value"])  

    df.to_csv("monthly_filled_performance.csv", sep='\t', index=False)
    print(f"Remaining players: {df['player_id'].nunique()}, Rows: {len(df)}")


if __name__ == "__main__":
    main()

