import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# --- Setup Chrome ---
def create_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"

    service = Service("/opt/homebrew/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://www.google.com")
    print("✅ Connected via:", driver.title)
    driver.quit()


BASE_URL = "http://ufcstats.com/statistics/events/completed"

def get_event_links(driver):
    driver.get(BASE_URL)
    time.sleep(2)
    event_links = []
    for a in driver.find_elements(By.CSS_SELECTOR, "a.b-link.b-link_style_black"):
        href = a.get_attribute("href")
        if "event-details" in href:
            event_links.append(href)
    return event_links

def get_fight_links(driver, event_url):
    driver.get(event_url)
    time.sleep(2)
    fight_links = []
    for a in driver.find_elements(By.CSS_SELECTOR, "a.b-flag.b-flag_style_green"):
        href = a.get_attribute("href")
        if "fight-details" in href:
            fight_links.append(href)
    return fight_links

def parse_fight(driver, fight_url):
    driver.get(fight_url)
    time.sleep(2)

    # fighter names
    fighters = [el.text.strip() for el in driver.find_elements(By.CSS_SELECTOR, "div.b-fight-details__person-name")]
    if len(fighters) < 2:
        return None

    # winner
    winner = None
    try:
        win_elem = driver.find_element(By.CSS_SELECTOR, "div.b-fight-details__person-status.b-fight-details__person-status_style_green")
        parent = win_elem.find_element(By.XPATH, "..")
        if "Red" in parent.text:
            winner = "Red"
        elif "Blue" in parent.text:
            winner = "Blue"
    except:
        winner = None

    # Totals row
    try:
        totals = driver.find_elements(By.XPATH, "//table[contains(@class,'b-fight-details__table')]//tr[td[contains(text(),'Totals')]]/td")
        totals_text = [t.text.strip() for t in totals]
    except:
        return None

    if len(totals_text) < 14:
        return None

    data = {
        "fight_url": fight_url,
        "fighter_red": fighters[0],
        "fighter_blue": fighters[1],
        "winner": winner,
        "KD_red": totals_text[0],
        "KD_blue": totals_text[1],
        "SigStr_red": totals_text[2],
        "SigStr_blue": totals_text[3],
        "TotalStr_red": totals_text[8],
        "TotalStr_blue": totals_text[9],
        "TD_red": totals_text[10],
        "TD_blue": totals_text[11],
        "SubAtt_red": totals_text[12],
        "SubAtt_blue": totals_text[13],
    }
    return data

def scrape_ufc_data(limit=2):
    driver = create_driver()
    all_fights = []
    event_links = get_event_links(driver)[:limit]

    for event in event_links:
        print(f"Scraping event: {event}")
        fight_links = get_fight_links(driver, event)
        for fight in fight_links:
            info = parse_fight(driver, fight)
            if info:
                all_fights.append(info)

    driver.quit()
    df = pd.DataFrame(all_fights)
    df.to_csv("data/ufc_fights_raw.csv", index=False)
    print(f"✅ Saved {len(df)} fights to data/ufc_fights_raw.csv")

if __name__ == "__main__":
    scrape_ufc_data(limit=2)
