import PrizePicks


class PrizePicksEntry:
    def __init__(self, information: dict[str, dict[str, any]]):
        self.pick_information = information
        self.pick_string = ""
        self.pick_id = 0
        self.player_id = 0

        self.display_name = ""
        self.players = []

        self.line_score = 0
        self.stat_type = ""

        self.league = ""

        self.initialize_pick_information()

    def initialize_pick_information(self) -> None:
        self.pick_id = self.pick_information['id']
        self.player_id = self.pick_information['relationships']['new_player']['data']['id']
        player_information = PrizePicks.player_data_dict[self.player_id]

        self.display_name = player_information['attributes']['display_name']

        for name in self.display_name.split('+'):
            self.players.append(name.strip())

        self.line_score = float(self.pick_information['attributes']['line_score'])
        self.stat_type = self.pick_information['attributes']['stat_type']

        self.pick_string = f"{self.display_name} - {self.line_score} {self.stat_type}"

        league_id = self.pick_information['relationships']['league']['data']['id']
        self.league = PrizePicks.league_id_dict[league_id]
