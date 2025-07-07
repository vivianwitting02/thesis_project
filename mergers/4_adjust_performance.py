"""
Created by: Vivian Witting
Date: 28/05/2025

* This file transforms the final score into multiple variables: Team goals, Opponent goals, Match points
* Removes the (A) or (H) after each opponents team
* Orders the matches by date
* Replaces the "-" for "0" for data consistency
"""

import pandas as pd

def extract_match_info(row):
    score = row['score']
    opponent_info = row['opponent']

    new_opponent = row['opponent'].strip().split(' (')[0]
    
    try:
        goals_1, goals_2 = map(int, score.strip().split(' - '))
    except ValueError:
        return pd.Series([None, None, None, None])

    is_home = '(H)' in opponent_info
    team_goals = goals_1 if is_home else goals_2
    opponent_goals = goals_2 if is_home else goals_1

    if team_goals > opponent_goals:
        match_points = 3
    elif team_goals == opponent_goals:
        match_points = 1
    else:
        match_points = 0

    return pd.Series([new_opponent, team_goals, opponent_goals, match_points])


def main():

    df = pd.read_csv("../databases/all_200_players/extra_performance.csv", sep='\t')

    df[['opponent', 'team_goals', 'opponent_goals', 'match_points']] = df.apply(extract_match_info, axis=1)
    df['match_date'] = pd.to_datetime(df['match_date'], format='%d-%m-%Y', errors='coerce')
    
    invalid_dates = df[pd.to_datetime(df['match_date'], errors='coerce').isna()]
    print(invalid_dates[['match_date']])

    df = df.sort_values(by=['player_id', 'match_date'], ascending=[True, True])
    df = df.reset_index(drop=True)

    start_date = pd.to_datetime('2024-06-01')
    end_date = pd.to_datetime('2025-04-01')
    df = df[(df['match_date'] >= start_date) & (df['match_date'] <= end_date)]

    columns_to_replace = ['goal_total', 'assist', 'yellow_card', 'red_card', 'aerial_won', 'shots_total', 'pass_success']
    df[columns_to_replace] = df[columns_to_replace].replace('-', 0)

    df.to_csv('extra_clean.csv', index=False, sep='\t')


if __name__ == "__main__":
    main()