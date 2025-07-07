"""
Created by: Vivian Witting
Date: 28/05/2025

* This file scrapes all the market values overtime, from the top 225 listed Center Forwards (CF)
* This data is scraped from: https://www.footballtransfers.com
"""

import time
import json
import base64
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
options.add_extension('adblocker.crx')
driver = webdriver.Chrome(options=options)

base_url = "https://www.footballtransfers.com/en/values/players/most-valuable-players/striker-center"


# Accepting the cookies on footballtransfers.com using Selenium
def accept_cookies_football():
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))

    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframes[1])

    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, " css-47sehv"))
        )
        button.click()
        print("Clicked the 'Accepteer' button successfully!")
    except Exception as e:
        print("Error clicking the button:", e)

    driver.switch_to.default_content()


# Retrieve all the players links using BeautifulSoup on each page separately and append to list.
def scrape_player_links():
    soup = BeautifulSoup(driver.page_source, "html.parser")

    body = soup.find(id='player-table-body')
    players = body.find_all(attrs={'class': 'd-flex align-items-center'})
    player_links = []

    for name in players:
        link = name.find_all('a')
        player_name = link[0]['title']
        player_links.append((player_name, link[0]["href"]))
    
    return player_links


# For each players' link, get the market values using BeautifulSoup.
def scrape_market_values(player_url):
    driver.get(player_url)
    
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-base64]'))
    )
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    data_div = soup.find("div", {"data-base64": True})

    if not data_div:
        print("Market value graph data not found.")
        return None

    base64_data = data_div["data-base64"]
    decoded_data = base64.b64decode(base64_data).decode("utf-8")
    data_json = json.loads(decoded_data)
    print(f"Got JSON data for {player_url}")

    market_values = [
        {"date": point["x"], "value": point["y"]}
        for entry in data_json.get("dataSets", [])
        for point in entry.get("data", [])
        if point.get("y") is not None and point.get("x") is not None
    ]

    if not market_values:
        print("No market value data found.")
        return None

    lines = [[]]
    current_date = market_values[0]['date'].split('-')[1]

    for mv in market_values:
        new_date = mv['date'].split('-')[1]

        if new_date < current_date:
            lines.append([])

        lines[-1].append(mv)
        current_date = new_date

    if len(lines) > 2:
        return lines[2]
    else:
        return None


# Fix the dates from '25 to 2025 for continuity.
def fix_date(date):
    month, year_suffix = date.split("-'")
    year = int("20" + year_suffix)  # assumes 2000s
    month = int(month)
    return datetime.datetime(year, month, 1)


# For all 10 pages, loop over player links and get the market values accordingly.
# This data is stored in ../databases/part_two/all_market_values.csv
def main():
    for i in range(1, 10):
        if i == 1:
            driver.get(base_url)
            accept_cookies_football() 
        else:
            driver.get(f'{base_url}/{i}')

        time.sleep(10)

        player_links = scrape_player_links()
        final_list = []

        if player_links:
            for name, link in player_links:
                marktet_values = scrape_market_values(link)
                if marktet_values:
                    final_list.append([name, marktet_values])

        rows = []
        for player, records in final_list:
            for record in records:
                date = fix_date(record["date"])
                rows.append({'player': player, 'date': date, 'value': record['value']})

        df = pd.DataFrame(rows)
        df.to_csv("../databases/part_two/all_market_values.csv", sep='\t', mode='a',encoding='utf-8')

    driver.quit()


if __name__ == "__main__":
    main()
