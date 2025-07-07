"""
Created by: Vivian Witting
Date: 28/05/2025

* This file scrapes performance using the player_id's from whoscored.com
* The variables consist of: "league", "opponent", "score", "match_date", 
            "mins_played", "goal_total", "assist", "yellow_card", "red_card", 
            "shots_total", "pass_success", "aerial_won", "rating"
"""


import csv
import time
import pandas as pd
from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
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


def get_player_performance(player_id):
    url = f'https://www.whoscored.com/players/{player_id}/matchstatistics/'
    print(url)
    driver.get(url)
    time.sleep(3)

    headers = ["player_id", "league", "opponent", "score", "match_date", "mins_played", "goal_total",
               "assist", "yellow_card", "red_card", "shots_total", "pass_success",
               "aerial_won", "rating"]

    select_element = driver.find_element(By.CSS_SELECTOR, "dl#tournamentOptions select")
    options_count = len(Select(select_element).options)

    for i in range(options_count):
        select_element = driver.find_element(By.CSS_SELECTOR, "dl#tournamentOptions select")
        select = Select(select_element)
        option_text = select.options[i].text
        print("Selecting:", option_text)
        select.select_by_index(i)
        time.sleep(2)
        body_content = driver.find_element(By.ID, "player-table-statistics-body")
        match_rows = body_content.find_elements(By.TAG_NAME, "tr")

        with open("../databases/all_200_players/extra_performance.csv", 'a+', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers, delimiter='\t')
            if file.tell() == 0:
                writer.writeheader()

            for match in match_rows:
                try:
                    match_info = match.find_element(By.CLASS_NAME, "player-match-link").text
                    match_date = match.find_element(By.CLASS_NAME, "date").text
                    opponent = match_info.split("\n")[0]
                    score = match_info.split("\n")[1]
                    mins_played = match.find_element(By.CLASS_NAME, "minsPlayed").text
                    goal_total = match.find_element(By.CLASS_NAME, "goalTotal").text
                    assist = match.find_element(By.CLASS_NAME, "assist").text
                    yellow_card = match.find_element(By.CLASS_NAME, "yellowCard").text
                    red_card = match.find_element(By.CLASS_NAME, "redCard").text
                    shots_total = match.find_element(By.CLASS_NAME, "shotsTotal").text
                    pass_success = match.find_element(By.CLASS_NAME, "passSuccess").text
                    aerial_won = match.find_element(By.CLASS_NAME, "duelAerialWon").text
                    rating = match.find_element(By.CLASS_NAME, "rating").text

                    match_data = {
                        "player_id": player_id,
                        "league": option_text,
                        "opponent": opponent,
                        "score": score,
                        "match_date": match_date,
                        "mins_played": mins_played,
                        "goal_total": goal_total,
                        "assist": assist,
                        "yellow_card": yellow_card,
                        "red_card": red_card,
                        "shots_total": shots_total,
                        "pass_success": pass_success,
                        "aerial_won": aerial_won,
                        "rating": rating
                    }
                    writer.writerow(match_data)

                except Exception as e:
                    print(f"Error reading match row: {e}")




def main():
    names_1 = pd.read_csv('../databases/names_1.csv', sep=', ', engine='python', encoding='utf-8')
    names_2 = pd.read_csv('../databases/names_2.csv', sep=', ', engine='python', encoding='utf-8')
    # names_3 = pd.read_csv('../databases/extra_names.csv', sep=', ')

    names_combined = pd.concat([names_1, names_2], ignore_index=True)

    pass_cookies()

    # Loop through the combined DataFrame
    for _, row in names_combined.iterrows():
        player_id = row['player_id']
        get_player_performance(player_id)

    driver.quit()


if __name__ == "__main__":
    main()
