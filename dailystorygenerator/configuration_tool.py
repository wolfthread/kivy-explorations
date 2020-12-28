from pathlib import Path
import shutil
import json

import kivy
kivy.require("1.9.0")
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.properties import ListProperty, StringProperty


WORKING_DIRECTORY = None

with open("config.json") as config_f:
    json_data = config_f.read()

PARAMETERS = json.loads(json_data)

HEROES_FILE = PARAMETERS["HEROES_FILE"]
CITIES_FILE = PARAMETERS["CITIES_FILE"]
TRIGGERS_FILE = PARAMETERS["TRIGGERS_FILE"]
BEGINNINGS_FILE = PARAMETERS["BEGINNINGS_FILE"]
THEMES_FILE = PARAMETERS["THEMES_FILE"]
CHOICE = None
# COLOR_SHADE_1 = PARAMETERS["COLOR_SHADE_1"]
# COLOR_SHADE_2 = PARAMETERS["COLOR_SHADE_2"]
# COLOR_SHADE_3 = PARAMETERS["COLOR_SHADE_3"]
# COLOR_SHADE_4 = PARAMETERS["COLOR_SHADE_4"]


def on_save_button():
    the_popup = ShowSavedPopup()
    the_popup.open()


def copy_file(filename_src, filename_dst ):
    data_folder = Path("img/")
    try:
        shutil.copy2(filename_src, data_folder / '{}.jpg'.format(filename_dst))
    except:
        pass




def remove_from_file(directory, filename, list_of_items, item_to_remove):
    if not directory:
        complete_filename = filename
    else:
        complete_filename = directory+"/"+filename
    with open(complete_filename, "w") as f_w:
        for i in range(len(list_of_items)):
            current = list_of_items[i]
            if current != item_to_remove and i < len(list_of_items)-2:
                f_w.write(current+"\n")
            elif current != item_to_remove:
                f_w.write(current)


def append_to_file(name):
    with open(WORKING_DIRECTORY + "/" + HEROES_FILE, "a+") as f_hero:
        f_hero.write(name)


def create_defaults(directory):
    list_of_files = [CITIES_FILE, HEROES_FILE,
                     TRIGGERS_FILE, BEGINNINGS_FILE]
    for item in list_of_files:
        with open(directory + "/" + item, "w") as f:
            pass

def create_dir(directory):
    global WORKING_DIRECTORY
    Path(directory).mkdir(parents=True, exist_ok=True)
    WORKING_DIRECTORY = directory


def write_to_file(filename, line):
    global WORKING_DIRECTORY
    with open(WORKING_DIRECTORY + "/" + filename, "a+") as f:
        f.write(line)



class DeleteTheme(Screen):
    stored_themes = ListProperty()

    def on_enter(self, *args):
        with open(THEMES_FILE) as f:
            self.stored_themes = f.read().splitlines()

    def args_converter(self, row_index, an_obj):
        return {'text': an_obj,
                'size_hint_y': None,
                'height': 25,
                'on_press': self.delete_theme}

    def delete_theme(self, *args):
        theme = args[0].text
        shutil.rmtree(theme)
        with open(THEMES_FILE, "r") as f_r:
            all_themes_stored = f_r.read().splitlines()
        remove_from_file('',THEMES_FILE,all_themes_stored,theme)
        # with open(THEMES_FILE, "w") as f_w:
        #     for i in range(len(all_themes_stored)):
        #         current = all_themes_stored[i]
        #         if current != theme and i < len(all_themes_stored)-2:
        #             f_w.write(current+"\n")
        #         elif current != theme:
        #             f_w.write(current)

    #  missing a delete images function, to be run before we delete the directory

class ModifyThemePopup(Popup):
    global WORKING_DIRECTORY
    stored_heroes = ListProperty()
    stored_cities = ListProperty()
    stored_triggers = ListProperty()
    stored_beginnings = ListProperty()

    def __init__(self, **kwargs):
        super(ModifyThemePopup, self).__init__(**kwargs)
        self.old_value = None
        with open(WORKING_DIRECTORY+"/"+HEROES_FILE) as f:
            self.stored_heroes = f.read().splitlines()
        with open(WORKING_DIRECTORY+"/"+CITIES_FILE) as f:
            self.stored_cities = f.read().splitlines()
        with open(WORKING_DIRECTORY+"/"+TRIGGERS_FILE) as f:
            self.stored_triggers = f.read().splitlines()
        with open(WORKING_DIRECTORY+"/"+BEGINNINGS_FILE) as f:
            self.stored_beginnings = f.read().splitlines()

    def write_list_to_file(self, complete_filename, list_of_items):
        with open(complete_filename, "w") as f_w:
            for i in range(len(list_of_items)):
                current = list_of_items[i]
                if i < len(list_of_items) - 1:
                    f_w.write(current + "\n")
                else:
                    f_w.write(current)

    def replace_in_file(self, old, new):
        if old in self.stored_heroes:
#            print(self.stored_heroes)
#            remove_from_file(WORKING_DIRECTORY, HEROES_FILE, self.stored_heroes, old)
            self.stored_heroes.remove(old)
            self.stored_heroes.append(new)
#            print(self.stored_heroes)
            self.write_list_to_file(WORKING_DIRECTORY+"/"+HEROES_FILE, self.stored_heroes)
        elif old in self.stored_cities:
            self.stored_cities.remove(old)
            self.stored_cities.append(new)
            self.write_list_to_file(WORKING_DIRECTORY+"/"+CITIES_FILE, self.stored_cities)
        elif old in self.stored_beginnings:
            self.stored_beginnings.remove(old)
            self.stored_beginnings.append(new)
            self.write_list_to_file(WORKING_DIRECTORY+"/"+BEGINNINGS_FILE, self.stored_beginnings)
        elif old in self.stored_triggers:
            self.stored_triggers.remove(old)
            self.stored_triggers.append(new)
            self.write_list_to_file(WORKING_DIRECTORY+"/"+TRIGGERS_FILE, self.stored_triggers)

    def replace(self):
        new = self.ids.new_value.text
        # print("new: ", new)
        # print("old: ", self.old_value)
        # print(WORKING_DIRECTORY)
        self.replace_in_file(self.old_value, new)

    def set_old_value(self, an_obj):
        self.old_value = an_obj.text

    def args_converter(self, row_index, an_obj):
        return {'text': an_obj,
                'size_hint_y': None,
                'height': 25,
                'on_press': self.set_old_value}



class ModifyTheme(Screen):
    stored_themes = ListProperty()

    def on_enter(self, *args):
        with open(THEMES_FILE) as f:
            self.stored_themes = f.read().splitlines()

    def args_converter(self, row_index, an_obj):
        return {'text': an_obj,
                'size_hint_y': None,
                'height': 25,
                'on_press': self.open_modify}

    def open_modify(self, an_obj):
        global WORKING_DIRECTORY
        WORKING_DIRECTORY = an_obj.text
        the_popup = ModifyThemePopup()
        the_popup.open()


class ModifyScreen(Screen):
    pass

class Intro(Screen):
    pass

class CreateTheme(Screen):

    def create_shells(self):
        try:
            self.custom_theme = self.ids.custom_theme.text
            create_dir(self.custom_theme)
            create_defaults(self.custom_theme)
            with open(THEMES_FILE) as f:
                menu = f.readlines()
            if not self.custom_theme in menu:
                with open(THEMES_FILE, 'a+') as config_f:
                    config_f.write("\n"+self.custom_theme)
                return True
        except:
            return False


class Error(Screen):
    pass


class ShowSavedPopup(Popup):
    def __init__(self, **kwargs):
        super(ShowSavedPopup, self).__init__(**kwargs)
        Clock.schedule_once(self.dismiss_popup, 0.2)

    def dismiss_popup(self, dt):
        self.dismiss()


class HeroCreatorPopup(Popup):

    def copy_hero_file(self, filename):
        copy_file(filename, '{}'.format(self.ids.hero_name.text))
        on_save_button()

    def copy_villain_file(self, filename):
        copy_file(filename, '{}'.format(self.ids.villain_name.text))
        on_save_button()

    def write_hero(self):  # clean this up as doubling
        try:
            if self.ids.hero_name.text:
                append_to_file("{}:".format(self.ids.hero_name.text))
                on_save_button()
        except:
            pass

    def write_villain(self):
        try:
            if self.ids.villain_name.text:
                append_to_file("{}\n".format(self.ids.villain_name.text))
                on_save_button()
        except:
            pass


class DSGConfigurationTool(Screen):
    # color_shade_1 = ListProperty()
    # color_shade_2 = ListProperty()
    # color_shade_3 = ListProperty()
    # color_shade_4 = ListProperty()

    def __init__(self, **kwargs):
        super(DSGConfigurationTool, self).__init__(**kwargs)
        pass
        # self.color_shade_1 = COLOR_SHADE_1
        # self.color_shade_2 = COLOR_SHADE_2
        # self.color_shade_3 = COLOR_SHADE_3
        # self.color_shade_4 = COLOR_SHADE_4

    def hero_and_villain_creator(self):
        the_popup = HeroCreatorPopup()
        the_popup.open()

    def write_cities(self):
        try:
            if self.ids.city_name.text:
                write_to_file("cities.txt", "{}\n".format(self.ids.city_name.text))
                on_save_button()
        except:
            pass

    def write_story_beg(self):
        try:
            if self.ids.story_beginning.text:
                write_to_file("beginnings.txt", "{}\n".format(self.ids.story_beginning.text))
                on_save_button()
        except:
            pass

    def write_trigger(self):
        try:
            if self.ids.trigger.text:
                write_to_file("triggers.txt", "{}\n".format(self.ids.trigger.text))
                on_save_button()
        except:
            pass


class ConfigScreenManager(ScreenManager):
    pass


buildKV = Builder.load_file("configscreenmanager.kv")
# add another kv file: "custom_widgets.kv" to prevent repetitions

class DSGConfigurationToolApp(App):

    def build(self):
        self.title = "DailyStoryGenerator Configuration Tool"
        return buildKV

def main():
    DSGConfigurationToolApp().run()


if __name__ == '__main__':
    DSGConfigurationToolApp().run()