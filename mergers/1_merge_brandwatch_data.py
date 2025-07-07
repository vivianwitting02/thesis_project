"""
Created by: Vivian Witting
Date: 28/05/2025

* This file merges all the different brandwatch data files together into one file: 
* all_brandwatch.csv containing 203 different player IDs "complete_brandwatch_df.csv"
"""

import pandas as pd
import os

# Helper to process individual mention files
def get_dataframe(file_path, skip_rows, value_name):
    df_raw = pd.read_csv(file_path, skiprows=skip_rows, header=None)
    df_raw = df_raw.dropna(how='all', axis=1)
    df_raw = df_raw.rename(columns={0: 'player_id'})
    df_long = df_raw.melt(id_vars=['player_id'], var_name='day', value_name=value_name)
    df_long['day'] = pd.to_numeric(df_long['day'], errors='coerce')
    df_long = df_long.dropna(subset=['day'])

    start_date = pd.to_datetime('2024-06-01')
    df_long['date'] = start_date + pd.to_timedelta(df_long['day'], unit='D')
    return df_long[['player_id', 'date', value_name]]

# Core function to compile data
def fix_frame():
    main_df = pd.DataFrame()

    for i in range(1, 8):
        base_path = f"../brandwatch/center_forward_{i}"

        files = {
            'total_mentions': ("overtime/mention_count.csv", 9),
            'pos_mentions': ("overtime/positive_overtime.csv", 10),
            'neg_mentions': ("overtime/negative_overtime.csv", 10),
            'total_X': ("difference/total_X.csv", 10),
            'pos_X': ("difference/positive_X_overtime.csv", 11),
            'neg_X': ("difference/negative_X_overtime.csv", 11),
            'total_news': ("difference/total_news.csv", 10),
            'pos_news': ("difference/positive_news_overtime.csv", 11),
            'neg_news': ("difference/negative_news_overtime.csv", 11),
            'total_reddit': ("difference/total_reddit.csv", 10),
            'pos_reddit': ("difference/positive_reddit_overtime.csv", 11),
            'neg_reddit': ("difference/negative_reddit_overtime.csv", 11),
        }

        dfs = []
        for col_name, (file_rel_path, skip) in files.items():
            file_path = os.path.join(base_path, file_rel_path)
            if os.path.exists(file_path):
                df = get_dataframe(file_path, skip, col_name)
                dfs.append(df)
            else:
                print(f"Missing file: {file_path}")

        if dfs:
            merged = dfs[0]
            for df in dfs[1:]:
                merged = merged.merge(df, on=['player_id', 'date'], how='outer')
            merged = merged[merged['date'].between('2024-06-01', '2025-04-01')]
            main_df = pd.concat([main_df, merged], ignore_index=True)

    return main_df

def main():
    df = fix_frame()
    df = df.sort_values(by=['player_id', 'date'])
    df.to_csv("complete_brandwatch_df.csv", sep='\t', index=False)

if __name__ == "__main__":
    main()
