import datetime
import os
import time

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

import ujson as json

# TODO: skim PrizePicks page / open most recent PrizePicks
# TODO: save PrizePicks info to file
# TODO: separate picks by sport

loaded_from_json = False


def scrape_prizepicks(force_scrape: bool = False) -> str:
    global loaded_from_json
    loaded_from_json = False

    prizepicks_file_url = "PrizePicks Content.json"

    # the number of minutes between each scrape of the site
    time_threshold = 30

    # creates the file if it does not exist and then forces a scrape
    if not os.path.exists(prizepicks_file_url):
        print("Does not exist")
        file = open(prizepicks_file_url, 'x')
        file.close()
        force_scrape = True

    # get the time the file was last written to
    last_written = datetime.datetime.fromtimestamp(os.path.getmtime(prizepicks_file_url))
    time_difference = datetime.datetime.now() - last_written

    # go to the site and scrape the picks
    if force_scrape or (time_difference.seconds / 60 > time_threshold):
        prizepicks_url = 'https://api.prizepicks.com/projections'

        print(f"Scraping {prizepicks_url}...")
        print("Getting projections from PrizePicks...")

        # open the site in a Chrome window
        # then get all the picks
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)
        driver.get(prizepicks_url)
        time.sleep(6.25)
        content = driver.find_element(by=By.XPATH, value="/html/body/pre").text

        driver.quit()

        save_prizepicks_content(prizepicks_file_url, content)

        return content

    # open the file to get the picks
    else:
        print(f"Not Scraping. Pulling data from {prizepicks_file_url}...")
        file = open(prizepicks_file_url, "r")

        # read each line of the file into the memory.
        # this can get expensive
        file_content = ""
        for line in file:
            line_content = line.strip()
            file_content += line_content
        file.close()

        # if successful, return the file content
        if file_content != "":
            loaded_from_json = True
            return file_content

        # if unsuccessful, run the function again, but force a scrape
        else:
            print(f"Could not successfully get content from {prizepicks_file_url}! Forcing scrape!")
            return scrape_prizepicks(force_scrape=True)


def save_prizepicks_content(path: str, content: str) -> None:
    global loaded_from_json

    if loaded_from_json:
        return

    # convert the content string to JSON
    json_content = json.loads(content)

    # write the JSON data to the file
    file = open(path, "w")
    json.dump(json_content, file, indent=4)
    file.close()
