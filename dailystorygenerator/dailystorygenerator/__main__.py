#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import storygenerator
import kivy
import sys
from pathlib import Path

kivy.require("1.9.0")
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen


DATA_FOLDER = Path("img/")

THEMES = []
with open("menu_themes.txt", "r") as f:
    THEMES += f.read().splitlines()

DEFAULT = THEMES[0]+"/"


CITY_FILE = "cities.txt"
HEROES_FILE = "heroes_and_villains.txt"
TRIGGERS_FILE = "triggers.txt"
BEG_FILE = "beginnings.txt"

def generate_story(choice):
    global CITY_FILE, HEROES_FILE, TRIGGERS_FILE, BEG_FILE
    new_story = storygenerator.Storygenerator(choice + "/" + CITY_FILE,
                                              choice + "/" + HEROES_FILE,
                                              choice + "/" + TRIGGERS_FILE,
                                              choice + "/" + BEG_FILE)
    new_story.change_theme(choice)

def image_to_open(name_image):
    path_to_image = DATA_FOLDER / "{}.jpg".format(name_image)
    return str(path_to_image)

def file_to_open(name_image):
    path_to_image = DATA_FOLDER / "{}.jpg".format(name_image)
    return str(path_to_image)


class BeginStoryPopUp(Popup):
    beginning = StringProperty()
    trigger = StringProperty()

    def __init__(self, **kwargs):
        super(BeginStoryPopUp, self).__init__(**kwargs)
        self.beginning = new_story.begininning
        self.name_villain = new_story.villain
        self.trigger = new_story.trigger


class StoryScreenPopup(Popup):
    contents = StringProperty()
    img_hero = StringProperty()
    img_villain = StringProperty()
    img_vs = StringProperty()
    name_hero = StringProperty()
    name_villain = StringProperty()
    name_city = StringProperty()

    def __init__(self, **kwargs):
        super(StoryScreenPopup, self).__init__(**kwargs)
        self.name_hero = new_story.hero
        self.name_villain = new_story.villain
        self.name_city = new_story.city
        self.img_hero = image_to_open(new_story.hero)
        self.img_villain = image_to_open(new_story.villain)
        self.img_vs = image_to_open("vs")


    def open_begin_story_popup(self):
        the_popup = BeginStoryPopUp()
        the_popup.open()


class IntroScreen(Screen):
    themes = ListProperty()
    new_story = ObjectProperty()

    def __init__(self, **kwargs):
        new_story = storygenerator.Storygenerator(DEFAULT + CITY_FILE, DEFAULT + HEROES_FILE,
                                                  DEFAULT + TRIGGERS_FILE, DEFAULT + BEG_FILE)
        super(IntroScreen, self).__init__(**kwargs)
        self.themes = new_story.themes

    def assign_choice(self, choice):

        new_story.load(choice+"/"+CITY_FILE, choice+"/"+HEROES_FILE,
                       choice+"/"+TRIGGERS_FILE, choice+"/"+BEG_FILE)
        new_story.change_theme(choice)

    def spinner_clicked(self, value):
        self.assign_choice(value)

class WelcomeScreen(Screen):
    img_bkg = "WELCOME.jpg"

    def random_hero(self):
        new_story.random_hero()


class ScrollingScreen(Screen):
    img_hero = StringProperty(None)
    img_villain = StringProperty(None)

    def random_hero(self):
        new_story.random_hero()


class MyScreenManager(ScreenManager):

    def new_hero(self):
        new_story.increase_scroller()
        scroller = new_story.scroller % len(new_story.all_heroes)
        img_hero = image_to_open(new_story.all_heroes[scroller])
        img_villain = image_to_open(new_story.all_villains[scroller])
        name = str(time.time())  # getting unique name
        s = ScrollingScreen(name=name)
        self.add_widget(s)
        self.current = name
        s.img_hero = img_hero
        s.img_villain = img_villain
        new_story.new_hero(new_story.all_heroes[scroller])

    def open_story_screen_popup(self):
        the_popup = StoryScreenPopup()
        the_popup.open()


buildKV = Builder.load_file("screenmanager.kv")

class StoryGeneratorApp(App):

    def build(self):
        self.title = "DailyStoryGenerator"
        return buildKV

if __name__ == '__main__':
    new_story = storygenerator.Storygenerator(DEFAULT+CITY_FILE, DEFAULT+HEROES_FILE,
                                              DEFAULT+TRIGGERS_FILE, DEFAULT+BEG_FILE)

    StoryGeneratorApp().run()
