import argparse
import typing
import PrizePicks as PP


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


def main(args):
    print(f"Parsed Args: {args}")

    print("Hello World!")

    PP.initialize(args['refresh'])

    league = input("League?: ")
    stat_type = input("Category?: ")
    pick_id = input("ID?: ")

    print(f"{PP.picks_dict[league][stat_type][pick_id]}")


    # TODO: ask user for which sport they want
    # TODO: show the picks for the given sport
    # TODO: get the stats for each team
    # TODO: get the stats for each player


if __name__ == '__main__':
    parsed_arguments = parse_arguments()
    main(parsed_arguments)
