import typing
from simple_term_menu import TerminalMenu


class MenuWrapperNode:
    def __init__(self, dictionary: dict[str, typing.Any], isHead = False, title=""):
        """
        MAKE THE DICTIONARY FIRST.
        THEN CONSTRUCT THE HEAD NODE.
        THEN CONSTRUCT THE WRAPPER CLASS.

        :param dictionary: keys - displayed elements values - things the menu returns
        """

        self.dictionary = dictionary

        self.add_back_to_dictionaries()

        # noinspection PyTypeChecker
        self.menu: TerminalMenu = TerminalMenu(self.dictionary.keys(), title=title)

        self.parent_menu = None

        self.wrapper = None

    def add_back_to_dictionaries(self):

        # for item in self.dictionary:
        #     if isinstance(item, MenuWrapperNode):
        #         item.add_back_to_dictionaries()

        self.dictionary["Back"] = MenuWrapper.go_back

    def add_key_to_menu(self, key: str, value: typing.Any):
        self.dictionary[key] = value

        # refresh menu

    def get_current_menu(self, path: list[str], up_or_down: bool = True):
        """

        :param path: The keys of the menus' dictionaries
        :param up_or_down: True = going up to the parent. False = going down to find the current menu
        :return: MenuWrapper of the current menu
        """

        # go to the menu of the current item
        # remove the current item from the path list
        # change directions and go down
        if self.parent_menu is None:
            if isinstance(self.dictionary[path[0]], MenuWrapperNode):
                return self.get_current_menu(path[1:], False)
            else:
                print(f"THE REST OF THE PATH IS NOT VALID: {path}")
                return self

        else:
            return self.parent_menu.get_current_menu(path, True)


class MenuWrapper:
    def __init__(self, head: MenuWrapperNode):
        self.head = head
        self.current_menu = self.head

        self.set_as_wrapper(self.head)

        # noinspection PyTypeChecker
        self.set_parents(current_node=self.head, previous_node=None)

    def set_as_wrapper(self, current_node: MenuWrapperNode):
        # set the node's wrapper
        current_node.wrapper = self

        # recursively set the children's wrappers
        for item in current_node.dictionary:
            if isinstance(item, MenuWrapperNode):
                self.set_as_wrapper(item)

    def set_parents(self, current_node: MenuWrapperNode, previous_node: MenuWrapperNode):

        current_node.parent_menu = previous_node

        # recursively set the children's parents
        for item in current_node.dictionary:
            if isinstance(current_node.dictionary[item], MenuWrapperNode):
                self.set_parents(current_node=current_node.dictionary[item], previous_node=current_node)

    def go_back(self) -> bool:
        if self.current_menu == self.head:
            return False

        self.current_menu = self.current_menu.parent_menu
        return True

    def show(self) -> typing.Any:
        while True:
            menu_key_index = self.current_menu.menu.show()

            menu_key = list(self.current_menu.dictionary.keys())[menu_key_index]
            menu_value = self.current_menu.dictionary[menu_key]

            if menu_value is None or menu_key == '':
                menu_value = menu_key

            if isinstance(menu_value, MenuWrapperNode):
                self.current_menu = menu_value

            elif menu_value == MenuWrapper.go_back:
                valid_back = self.go_back()
                if not valid_back:
                    return None

            else:
                break

        return menu_value
