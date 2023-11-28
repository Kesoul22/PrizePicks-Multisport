import datetime
import os
import time
import typing

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

import ujson as json

# TODO: skim PrizePicks page / open most recent PrizePicks
# TODO: save PrizePicks info to file
# TODO: separate picks by sport

loaded_from_file = False
prizepicks_file_url = "PrizePicks Content.json"
prizepicks_url = 'https://api.prizepicks.com/projections'
league_id_dict: dict[int, str] = {}

player_data_dict: dict[str, typing.Any] = {}


class PrizePicksEntry:
    def __init__(self, information: dict[str, dict[str, any]]):
        self.pick_information = information



def scrape_prizepicks(force_scrape: bool = False) -> str:
    global loaded_from_file, prizepicks_file_url, prizepicks_url
    loaded_from_file = False

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

        return content

    # open the file to get the picks
    else:
        print(f"Not Scraping. Pulling data from {prizepicks_file_url}...")
        file = open(prizepicks_file_url, "r")

        # read each line of the file into the memory.
        # this can get expensive
        content = ""
        for line in file:
            line_content = line.strip()
            content += line_content
        file.close()

        # if successful, return the file content
        if content != "":
            loaded_from_file = True

            return content

        # if unsuccessful, run the function again, but force a scrape
        else:
            print(f"Could not successfully get content from {prizepicks_file_url}! Forcing scrape!")
            return scrape_prizepicks(force_scrape=True)


def save_prizepicks_content(path: str, content: str) -> dict[str, typing.Any]:
    global loaded_from_file

    # convert the content string to JSON
    json_content = json.loads(content)

    if loaded_from_file:
        return json_content

    # write the JSON data to the file
    file = open(path, "w")
    json.dump(json_content, file, indent=4)
    file.close()

    return json_content


def convert_content_to_picks(json_content_dict: dict[str, typing.Any]) -> dict[str, dict[str, list[PrizePicksEntry]]]:
    global league_id_dict, player_data_dict

    # constant values for the IDs of each league
    ID_NFL = "1"
    ID_NBL = "1"
    ID_NHL = "1"
    ID_MLB = "1"

    # This is a list of all the picks as JSON objects
    projection_content = json_content_dict["data"]

    # this is a list of all the player information as JSON objects
    player_content = json_content_dict["included"]

    # key   :   player ID
    # value :   player information
    player_data_dict = {}

    # add all available players to the dictionary
    for item in player_content:
        # skip all non-player items
        if item['type'] != 'new_player':
            continue

        player_id = item['id']

        # place the player into the dictionary
        player_data_dict[player_id] = item

    # key   :   League string / id
    # value :   dictionary
    #       key     : string of category name
    #       value   : list of Picks
    picks_dict: dict[str, dict[str, list[PrizePicksEntry]]] = {}

    for item in projection_content:
        # skip non-projection items
        if item['type'] != 'projection':
            continue

        # skip all games that are currently being played
        if item['attributes']['status'] != "pre_game":
            continue

        player_id = item['relationships']['new_player']['data']['id']

        # add player names to array and add all names in combo
        player_names = []

        if player_data_dict[player_id]['attributes']['combo']:
            name_list = player_data_dict[player_id]['attributes']['display_name'].split("+")
            for name in name_list:
                player_names.append(name.strip())
        else:
            player_names.append(player_data_dict[player_id]['attributes']['display_name'])

        # store plyer data
        player_league = player_data_dict[player_id]['attributes']['league']
        player_team = player_data_dict[player_id]['attributes']['team_name']
        player_position = player_data_dict[player_id]['attributes']['position']
        player_projection = item['attributes']['line_score']
        player_time_date: str = item['attributes']['start_time'].split("T")
        player_date = player_time_date[0]
        player_time = player_time_date[1]
        player_versus = item['attributes']['description']
        player_stat_type = item['attributes']['stat_type']

        league_id = item['relationships']['league']['data']['id']

        # if the league info is not in the projection data, it will be in the player data
        try:
            league_name = item['attributes']['league']
        except KeyError:
            player_id = item['relationships']['new_player']['data']['id']
            league_name = player_data_dict[player_id]['attributes']['league']

        # add the league ID and name to the league ID dictionary
        league_id_dict[league_id] = league_name

        # if the pick's corresponding league is not in the dictionary,
        # add the league to the dictionary
        if league_name not in picks_dict:
            picks_dict[league_name] = dict()

        # create the pick
        entry: PrizePicksEntry = PrizePicksEntry(item)

        # store the stat category
        stat_category = item['attributes']['stat_type']

        if stat_category not in picks_dict[league_name]:
            picks_dict[league_name][stat_category] = []

        # add the pick to the corresponding league's list
        picks_dict[league_name][stat_category].append(entry)

    return picks_dict


def initialize(force_scrape):
    global prizepicks_file_url
    content = scrape_prizepicks(force_scrape=force_scrape)
    print()

    json_content = save_prizepicks_content(prizepicks_file_url, content)

    picks_dict: dict[str, dict[str, list[PrizePicksEntry]]] = convert_content_to_picks(json_content)

    for pick_id in picks_dict:
        print(f"{pick_id}")
        for stat_category in picks_dict[pick_id]:
            print(f"\t({len(picks_dict[pick_id][stat_category]).__str__().center(3)}) {stat_category.ljust(25)} : ", end="")
            for pick in picks_dict[pick_id][stat_category]:
                print(f"{pick.pick_information['id'].__str__().ljust(6)} ", end=" ")

                if pick.pick_information['attributes']['status'] != "pre_game":
                    print(pick.pick_information['attributes']['status'].__str__(), end="")
                    return

            print()
        print()
