import os

import clubs
import events
import fighters


def main():
    os.mkdir("fighters")
    os.mkdir("clubs")
    os.mkdir("events")
    fighters.fighters()
    clubs.clubs()
    events.events()


if __name__ == "__main__":
    main()
