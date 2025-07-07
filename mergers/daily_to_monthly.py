"""
Created by: Vivian Witting
Date: 28/05/2025

* This file retrieves the averages and sums from the daily dataset.
* Gets saved in monthly_player_dataset.csv
"""

import pandas as pd

numeric_cols = [
    'market_value', 'total_mentions', 'pos_mentions', 'neg_mentions',
    'total_X', 'pos_X', 'neg_X', 'total_news', 'pos_news', 'neg_news',
    'total_reddit', 'pos_reddit', 'neg_reddit',
    'mins_played', 'goal_total', 'assist', 'yellow_card', 'red_card',
    'shots_total', 'pass_success', 'aerial_won', 'rating',
    'team_goals', 'opponent_goals', 'match_points'
]

ordered_cols = [
    'player_id', 'player', 'age', 'height', 'nationality', 'current_team', 'month', 'market_value',
    'total_mentions', 'pos_mentions', 'neg_mentions',
    'total_X', 'pos_X', 'neg_X', 'total_news', 'pos_news', 'neg_news',
    'total_reddit', 'pos_reddit', 'neg_reddit',
    'yellow_card', 'red_card', 'team_goals', 'opponent_goals', 'n_matches',
    'goals_per_match', 'assists_per_match', 'shots_per_match',
    'aerials_won_per_match', 'pass_success_avg', 'rating_avg',
    'match_points', 'mins_played_avg'
]

def get_monthly_df(df):
    monthly_df = df.groupby(['player_id', 'month'], as_index=False).agg({
        'market_value': 'first',  # Take market value from first day of month
        'total_mentions': 'sum',
        'pos_mentions': 'sum',
        'neg_mentions': 'sum',
        'total_X': 'sum',
        'pos_X': 'sum',
        'neg_X': 'sum',
        'total_news': 'sum',
        'pos_news': 'sum',
        'neg_news': 'sum',
        'total_reddit': 'sum',
        'pos_reddit': 'sum',
        'neg_reddit': 'sum',
        'yellow_card': 'sum',
        'red_card': 'sum',
        'team_goals': 'sum',
        'opponent_goals': 'sum',
        'goal_total': 'sum',
        'assist': 'sum',
        'shots_total': 'sum',
        'aerial_won': 'sum',
        'pass_success': 'sum',
        'rating': 'sum',
        'match_points': 'sum',
        'mins_played': 'sum',
        'opponent': 'count',  # match count
        'age': 'last',
        'height': 'last',
        'player': 'last',
        'nationality': 'last',
        'current_team': 'last'
    })
    
    monthly_df.rename(columns={'opponent': 'n_matches'}, inplace=True)

    # Add averages
    monthly_df['goals_per_match'] = monthly_df['goal_total'] / monthly_df['n_matches']
    monthly_df['assists_per_match'] = monthly_df['assist'] / monthly_df['n_matches']
    monthly_df['shots_per_match'] = monthly_df['shots_total'] / monthly_df['n_matches']
    monthly_df['aerials_won_per_match'] = monthly_df['aerial_won'] / monthly_df['n_matches']
    monthly_df['pass_success_avg'] = monthly_df['pass_success'] / monthly_df['n_matches']
    monthly_df['rating_avg'] = monthly_df['rating'] / monthly_df['n_matches']
    monthly_df['mins_played_avg'] = monthly_df['mins_played'] / monthly_df['n_matches']

    return monthly_df.round(3)


def main():
    df = pd.read_csv("../dataframes/final_versions/daily_player_dataset.csv", sep='\t', parse_dates=['date'])
    df['month'] = df['date'].dt.to_period('M').astype(str)

    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

    monthly_df = get_monthly_df(df)
    monthly_df = monthly_df[ordered_cols]

    # Save
    monthly_df.to_csv("monthly_player_dataset.csv", sep='\t', index=False)
    print(monthly_df.head())


if __name__ == "__main__":
    main()