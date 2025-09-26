import os

from views.menus import Menus


def main() -> None:
    os.system("clear")
    menu = Menus()
    menu.run()


if __name__ == "__main__":
    main()
