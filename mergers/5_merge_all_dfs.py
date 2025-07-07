"""
Created by: Vivian Witting
Date: 28/05/2025

* This script processes market value, performance, brandwatch, and player characteristics data for 200 players.
* It generates a daily dataset with one row per player for each day in the specified date range.
* The final dataset is saved as 'daily_player_dataset.csv'.
"""

import pandas as pd

def main():
    brandwatch = pd.read_csv('../dataframes/all_200_players/all_brandwatch.csv', sep='\t', parse_dates=['date'])
    performance = pd.read_csv('../dataframes/all_200_players/all_performance.csv', sep='\t', parse_dates=['match_date'])
    characteristics = pd.read_csv('../dataframes/all_200_players/all_characteristics.csv', sep='\t')
    market_values = pd.read_csv('../dataframes/all_200_players/daily_market_values.csv', sep='\t', parse_dates=['date'])

    start_date = pd.to_datetime('2024-07-01')
    end_date = pd.to_datetime('2025-04-01')

    valid_ids = market_values['player_id'].unique()

    for dataset, name in zip([brandwatch, performance, characteristics], ['brandwatch', 'performance', 'characteristics']):
        missing_ids = set(valid_ids) - set(dataset['player_id'].unique())
        if missing_ids:
            print(f"Warning: Missing player_id(s) in {name}: {missing_ids}")
            valid_ids = list(set(valid_ids) - missing_ids)

    brandwatch = brandwatch[brandwatch['player_id'].isin(valid_ids)]
    performance = performance[performance['player_id'].isin(valid_ids)]
    characteristics = characteristics[characteristics['player_id'].isin(valid_ids)]
    market_values = market_values[market_values['player_id'].isin(valid_ids)]

    all_players = valid_ids
    all_dates = pd.date_range(start=start_date, end=end_date, freq='D')
    full_grid = pd.MultiIndex.from_product([all_players, all_dates], names=['player_id', 'date'])
    df_daily = pd.DataFrame(index=full_grid).reset_index()

    characteristics['height'] = characteristics['height'].str.replace('cm', '', regex=False).astype(int)

    df_daily = df_daily.merge(characteristics, how='left', on='player_id')
    df_daily = df_daily.merge(market_values, how='left', on=['player_id', 'date'])
    df_daily = df_daily.merge(brandwatch, how='left', on=['player_id', 'date'])

    performance = performance.rename(columns={'match_date': 'date'})
    df_daily = df_daily.merge(performance, how='left', on=['player_id', 'date'])

    df_daily = df_daily.drop(columns=['positions'])
    

    # Reorder columns as specified
    desired_order = [
        'player_id', 'player', 'current_team', 'age', 'height', 'nationality', 'date', 'market_value',
        'total_mentions', 'pos_mentions', 'neg_mentions', 'total_X', 'pos_X', 'neg_X', 
        'total_news', 'pos_news', 'neg_news', 'total_reddit', 'pos_reddit', 'neg_reddit', 
        'league', 'opponent', 'score', 'mins_played', 'goal_total', 'assist', 'yellow_card', 
        'red_card', 'shots_total', 'pass_success', 'aerial_won', 'rating', 'team_goals', 
        'opponent_goals', 'match_points'
    ]

    df_daily = df_daily[desired_order]
    df_daily.to_csv('daily_player_dataset.csv', sep='\t', index=False)

if __name__ == "__main__":
    main()
