"""
Created by: Vivian Witting
Date: 28/05/2025

* This file gets all market_values overtime, from all players
* To create a daily df, we perform interpolation between the monthly
updated market values.
"""

import pandas as pd

interpolation_start = '2024-03-01'  # To include earlier and later values in interpolation
interpolation_end = '2025-05-02'  
start_date = '2024-06-01'
end_date = '2025-04-01'

first = pd.read_csv('../dataframes/all_200_players/p1_100_market_with_id.csv', sep='\t', parse_dates=['date'])
second = pd.read_csv('../dataframes/all_200_players/p2_100_market_with_id.csv', sep='\t', parse_dates=['date'])

market_values = pd.concat([first, second], ignore_index=True)
market_values['date'] = pd.to_datetime(market_values['date'], errors='coerce')

# Drop duplicates and ensure no repeated player_id/date pairs
duplicates = market_values[market_values.duplicated(subset=['player_id', 'date'], keep=False)]
duplicates = duplicates.sort_values(['player_id', 'date'])

all_interp = []

# Interpolation for each player
for player_id, group in market_values.groupby('player_id'):
    group = group.set_index('date').sort_index()
    
    player_name = group['player'].iloc[0] 
    
    extended_range = pd.date_range(start=interpolation_start, end=interpolation_end, freq='D')
    group = group[['market_value']].reindex(extended_range)
    group['player_id'] = player_id
    group['player'] = player_name 
    group['market_value'] = group['market_value'].interpolate(method='linear').ffill().bfill()

    if group['market_value'].isna().any():
        print(f"NaNs remain after interpolation for player {player_id}")
        continue

    group['market_value'] = group['market_value'].astype(int)
    group = group.reset_index().rename(columns={'index': 'date'})

    group = group[(group['date'] >= pd.to_datetime(start_date)) & (group['date'] <= pd.to_datetime(end_date))]
    all_interp.append(group)

market_daily = pd.concat(all_interp, ignore_index=True)
market_daily.to_csv('daily_market_values.csv', sep='\t', index=False)
