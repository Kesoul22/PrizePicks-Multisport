import selenium
import ujson

# TODO: skim PrizePicks page / open most recent PrizePicks
# TODO: save PrizePicks info to file
# TODO: separate picks by sport

loaded_from_json = False


def scrape_prizepicks() -> str:
    global loaded_from_json

    prizepicks_url = 'https://api.prizepicks.com/projections'
    prizepicks_file_url = "PrizePicks Content.json"



    return
