import argparse
import typing
import PrizePicks as PP

from consolemenu import *
from consolemenu.items import *

from simple_term_menu import TerminalMenu
from MenuWrapper import *
import PrizePicksEntry


def parse_arguments() -> dict[str, typing.Any]:

    # set up the text that appears when the user passes -h
    help_program_name = "PrizePicks Multi-Sport Help Tool"
    help_description = ""
    help_epilog = ""

    parser = argparse.ArgumentParser(prog=help_program_name, description=help_description, epilog=help_epilog)

    # set up arguments
    parser.add_argument('--refresh', '-r', action=argparse.BooleanOptionalAction, default=False,
                        help='<Optional> Forces a new reading of the picks from PrizePicks.com')

    # parser.add_argument('--test', required=True, nargs='+', help='<Required> Set flag')

    # parse the arguments and convert them into a dictionary
    return vars(parser.parse_args())


def menu_test_1():
    # create the menu
    menu = ConsoleMenu(title="Title thing", subtitle="subtitle thing")

    # menu items
    menu_item = MenuItem("Menu item 1")

    selection_menu = SelectionMenu(["item1", "item2", "item3"])
    # A SubmenuItem lets you add a menu (the selection_menu above, for example)
    # as a submenu of another menu
    submenu_item = SubmenuItem("Submenu item", selection_menu, menu)

    menu.append_item(menu_item)
    menu.append_item(submenu_item)

    menu.show()


def main(args):
    print(f"Parsed Args: {args}")

    print("Hello World!")

    PP.initialize(args['refresh'])

    # initialize the menu
    # league -> category -> pick id
    pick_menu_dict = {}

    for league in PP.picks_dict:

        category_dict = {}

        for category in PP.picks_dict[league]:

            pick_id_dict: dict[str, PrizePicksEntry] = {}
            for pick_id in PP.picks_dict[league][category]:
                pick_id_dict[PP.picks_dict[league][category][pick_id].pick_string] = PP.picks_dict[league][category][pick_id]

            category_dict[category] = MenuWrapperNode(pick_id_dict, title=f"Picks for [{category}] ({league})")

        pick_menu_dict[league] = MenuWrapperNode(category_dict, title=f"Categories for [{league}]")

    menu_wrapper = MenuWrapper(MenuWrapperNode(pick_menu_dict, isHead=True, title="Leagues"))
    chosen_pick: PrizePicksEntry = menu_wrapper.show()

    print(f"{chosen_pick.pick_id} - {chosen_pick.display_name}")

    # TODO: get the stats for each team
    # TODO: get the stats for each player


if __name__ == '__main__':
    parsed_arguments = parse_arguments()
    main(parsed_arguments)
