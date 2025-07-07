"""
Created by: Vivian Witting
Date: 28/05/2025

* This files finds the matching id's to the surnames using the all_market_values and 
names_2 files for the second batch: 109 players
"""

import pandas as pd
import unicodedata

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()

def extract_surname(name):
    return remove_accents(name.strip().split()[-1])

def main():
    # Load the data
    market_df = pd.read_csv('../databases/part_two/all_market_values.csv', sep='\t', encoding='utf-8')
    names_df = pd.read_csv('../databases/names_2.csv', sep=', ', engine='python', encoding='utf-8')

    market_df.columns = market_df.columns.str.strip().str.lower()
    names_df.columns = names_df.columns.str.strip().str.lower()

    market_df['surname'] = market_df['player'].apply(extract_surname)
    names_df['surname'] = names_df['player'].apply(extract_surname)

    merged_df = pd.merge(market_df, names_df[['player_id', 'surname']], on='surname', how='left')

    # Find unmatched players
    unmatched = names_df[~names_df['surname'].isin(market_df['surname'])]
    if not unmatched.empty:
        print("Unmatched players (by surname):")
        for name in unmatched['player']:
            print(f" - {name}")

    merged_df = merged_df[merged_df['player_id'].notna()]

    # Save merged file
    merged_df.drop(columns=['surname'], inplace=True)
    merged_df.drop(columns=['unnamed: 0'], inplace=True)
    merged_df.to_csv("second_market_with_id.csv", sep='\t', index=False, encoding='utf-8')

    matched = merged_df[merged_df['player_id'].notna()]
    unique_matched = matched['player_id'].nunique()
    print(f"Number of unique player IDs matched: {unique_matched}")


    print("\nMerged file saved as 'market_values_with_ids.csv'")

if __name__ == "__main__":
    main()
