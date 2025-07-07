"""
Created by: Vivian Witting
Date: 03/07/2025

* This file checks the amount of correct and incorrect sentiment classifications
"""

import pandas as pd

filepath = "../dataframes/comments_unique.csv"

# Read the raw data
df = pd.read_csv(filepath, sep="\t")
correct = 0
incorrect = 0

for _, row in df.iterrows():
    if row["sentiment"] == row["brandwatch_sent"]:
        correct += 1
    else:
        incorrect += 1

print(f"Correct: {correct}")
print(f"Incorrect: {incorrect}")
