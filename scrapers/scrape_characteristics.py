"""
Created by: Vivian Witting
Date: 28/05/2025

* This file scrapes characteristics from Whoscored.com
* The variables consist of: "current_team", "age", "height", "nationality", "positions"
"""

import csv
import time
import pandas as pd
from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

current_date = None
articles = []
three_months = datetime.now() - timedelta(days=90)

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_extension('adblocker.crx')
driver = webdriver.Chrome(options=chrome_options)

ajax_url = 'https://www.whoscored.com/players/148503/matchstatistics/'
driver.get(ajax_url)


def pass_cookies():
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "qc-cmp2-summary-buttons"))
        )

        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@class=" css-1wc0q5e"]'))
        )

        accept_button.click()
    except Exception as e:
        print(f"Error accepting cookies: {e}")
        pass


def get_characteristics(player_id):
    url = f'https://www.whoscored.com/players/{player_id}/show/'
    print(url)
    driver.get(url)

    time.sleep(3)

    info_block = driver.find_element(By.CSS_SELECTOR, '.col12-lg-10.col12-m-10.col12-s-9.col12-xs-8').text

    current_team = age = height = nationality = positions = ""

    lines = info_block.split('\n')
    for line in lines:
        if line.startswith("Current Team:"):
            current_team = line.split("Current Team:")[1].strip()
        elif line.startswith("Age:"):
            birth = line.split("Age:")[1].strip()
            age = birth.split(" ")[0]
        elif line.startswith("Height:"):
            height = line.split("Height:")[1].strip()
        elif line.startswith("Nationality:"):
            nationality = line.split("Nationality:")[1].strip()
        elif line.startswith("Positions:"):
            positions = line.split("Positions:")[1].strip()

    headers = ["player_id", "current_team", "age", "height", "nationality", "positions"]

    with open("../databases/all_200_players/all_characteristics.csv", 'a+', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers, delimiter='\t')
        if file.tell() == 0:
            writer.writeheader()

        writer.writerow({
            'player_id': player_id,
            'current_team': current_team,
            'age': age,
            'height': height,
            'nationality': nationality,
            'positions': positions
        })


def main():
    names_1 = pd.read_csv('../databases/extra_names.csv', sep=', ', engine='python', encoding='utf-8')
    # names_2 = pd.read_csv('../databases/names_2.csv', sep=', ', engine='python', encoding='utf-8')

    # names_combined = pd.concat([names_1, names_2], ignore_index=True)

    pass_cookies()

    # Loop through the combined DataFrame
    for _, row in names_1.iterrows():
        player_id = row['player_id']
        get_characteristics(player_id)

    driver.quit()

if __name__ == "__main__":
    main()
