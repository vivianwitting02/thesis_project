"""
Created by: Vivian Witting
Date: 28/05/2025

* This file forward fills the performance data per match,
to prevent the data from containing too many nan values.
"""

import pandas as pd

columns_to_drop = [
    'league', 'team_goals', 'opponent_goals', 'opponent',
    'score', 'yellow_card', 'red_card'
]

columns_to_fill = [
    'mins_played', 'goal_total', 'assist', 'shots_total', 
    'pass_success', 'aerial_won', 'rating', 'match_points'
]

def main():

    daily_df = pd.read_csv("../dataframes/final_versions/daily_player_dataset.csv", sep="\t")
    daily_df['date'] = pd.to_datetime(daily_df['date'])

    daily_df = daily_df.drop(columns=[col for col in columns_to_drop if col in daily_df.columns])
    daily_df = daily_df.sort_values(by=['player_id', 'date'])

    daily_df[columns_to_fill] = (
        daily_df.groupby('player_id')[columns_to_fill]
        .transform(lambda group: group.ffill().bfill())
    )

    daily_df.to_csv("daily_filled_performance.csv", sep='\t', index=False)
    print("Filled performance data saved to daily_filled_performance.csv")


if __name__ == "__main__":
    main()
