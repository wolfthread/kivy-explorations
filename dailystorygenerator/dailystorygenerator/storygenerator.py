import random
"""
This module generates daily story object, which constitutes of
a hero and villain pair, the beginning of a story as well as a story trigger,
all taken from user inputs when creating a theme.
"""

def from_file_to_dict(filename):
    content_as_dict = {}
    with open(filename, "r") as f:
        content = f.read().splitlines()
    for line in content:
        this_line = line.split(":")
        content_as_dict[this_line[0]] = this_line[1]
    return content_as_dict

def shuffle_and_get(a_list, num):
    random.shuffle(a_list)
    return a_list[:num]

class Storygenerator:

    def __init__(self, cities_file, heroes_file, triggers_file, beginnings_file):
        self.load(cities_file, heroes_file, triggers_file, beginnings_file)

    def load(self, cities_file, heroes_file, triggers_file, beginnings_file):
        self.cities_file, self.heroes_file, self.triggers_file, self.beginnings_file = [cities_file,
                                                                                        heroes_file,
                                                                                        triggers_file,
                                                                                        beginnings_file]

        # added this
        self.themes = []
        # need exception here if file is deleted, create new one with default values
        with open("menu_themes.txt", "r") as f:
            self.themes += f.read().splitlines()
        self.theme = self.themes[0]
        self.scroller = 0
        with open(self.cities_file, "r") as f:
            cities = f.read().splitlines()
        self.city = shuffle_and_get(cities, 1)[0]
        with open(self.beginnings_file, "r") as f:
            beginnings = f.read().splitlines()
        self.begininning = shuffle_and_get(beginnings, 1)[0]
        self.all_heroes_and_villains = from_file_to_dict(self.heroes_file)
        self.all_heroes = list(self.all_heroes_and_villains.keys())
        self.all_villains = list(self.all_heroes_and_villains.values())
        with open(self.triggers_file, "r") as f:
            triggers = f.read().splitlines()
        self.trigger = shuffle_and_get(triggers, 1)[0]
        self.random_hero()

    def random_hero(self):
        rand_choice = random.randint(0, len(self.all_heroes_and_villains) - 1)
        self.hero = list(self.all_heroes_and_villains.keys())[rand_choice]
        self.villain = self.all_heroes_and_villains[self.hero]

    def new_hero(self, choice):
        self.hero = choice
        self.villain = self.all_heroes_and_villains[self.hero]

    def increase_scroller(self):
        self.scroller += 1

    def add_theme(self,theme_to_add):
        self.themes.append(theme_to_add)

    def change_theme(self, theme_to_change):
        self.theme = theme_to_change


    def __str__(self):
        return "Hero: {}\nVillain: {}\nCity: {}\nBeginnings: {}\nTrigger: {}\nTheme: {}".format(self.hero,
                                                                                                self.villain,
                                                                                                self.city,
                                                                                                self.begininning,
                                                                                                self.trigger,
                                                                                                self.theme)
    def __repr__(self):
        return str(self)