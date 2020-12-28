"""
TeamMaker module. Contains both the gui and program logic for team making.
"""

import random
import kivy
import json
import member, team, colormaker
import datetime
from pathlib import Path

kivy.require("1.9.0")
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty


#Window.size = (600, 600)

# setting default language as English
LANG_CHOSEN = "en"
NOW = datetime.datetime.now().strftime("%d-%m-%Y__%H_%M_%S")

# Method to open file using pathlib
def open_a_file(folder_path, filename):
    data_folder = Path(folder_path)
    file_to_open = data_folder / filename
    return file_to_open

# pulling texts from files to default values
instructions_to_open = open_a_file("teammaker/data/texts/{}/".format(LANG_CHOSEN), "instructions.txt")
all_texts_to_open = open_a_file("teammaker/data/texts/{}/".format(LANG_CHOSEN), "all_texts.json")

with open(instructions_to_open) as f_inst:
    INSTRUCTIONS = f_inst.read()
with open(all_texts_to_open) as f_txt:
    json_data = f_txt.read()

ALL_TEXTS = json.loads(json_data)

LOW_CHOICE_RGB = 90
HIGH_CHOICE_RGB = 230
NUM_COLOR = 20

def random_choice_color():
    """Method returning a list of colors generated with the colormaker."""

    colors = list(colormaker.Colormaker(NUM_COLOR, LOW_CHOICE_RGB, HIGH_CHOICE_RGB))
    return random.choice(colors)[0], random.choice(colors)[1], random.choice(colors)[2]

# Popup classes
class LaguagePopup(Popup):
    """Initiates the language chosen by user"""
    pass

class InstructionsPopup(Popup):
    """Class pulling our the instructions of TeamMaker."""

    # Prompts
    title = INSTRUCTIONS
    instructions = ALL_TEXTS["instr_ttl"]


class TeamsMadePopup(Popup):
    """Popup presenting the results"""

    # Prompts
    contents = StringProperty()
    title = ALL_TEXTS["teamsmade_ttl"]

    # randomizing colors
    bground_color_r, bground_color_g, bground_color_b = random_choice_color()

    def __init__(self, **kwargs):
        super(TeamsMadePopup, self).__init__(**kwargs)
        save_file = open_a_file("teammaker/save/", "teams.txt")
        with open(save_file) as f:
            self.contents = f.read()

class NamesPopup(Popup):
    """Popup prompting user to enter names"""

    # Prompts
    title = ALL_TEXTS["names_ttl"]
    submit_btn_txt = ALL_TEXTS["submit_btn"]

    def register(self):
        self.names = self.ids.names.text
        names_saved = open_a_file("teammaker/save/", "names.txt")
        f = open(names_saved, "w+")
        f.write(self.names)
        f.close()


class TeamsPopup(Popup):
    """Team popup containing the TeamMaker methods."""

    # Prompts
    title = ALL_TEXTS["teams_ttl"]
    ready_btn_txt = ALL_TEXTS["teams_ready_btn"]

    def open_teams_made_popup(self):
        the_popup = TeamsMadePopup()
        the_popup.open()

    def make_teams(self):
        persons = []
        self.teams = []

        # capturing values from app inputs
        app = App.get_running_app()
        num_persons = app.root.ids.num_persons.value
        split_mode_val = app.root.ids.split_mode_num.value
        mixing_mode = app.root.ids.mix_mode.text
        split_mode = app.root.ids.split_mode.text

        # ------------------------ TeamMaker methods--------------------------------

        # pulling names from file
        read_names = open_a_file("teammaker/save/", "names.txt")
        with open(read_names) as f:
            for line in f:
                name = line.split()
                if len(name) != 1:
                    current_member = member.Member(name[0], name[1])
                else:
                    current_member = member.Member(name[0])
                persons.append(current_member)

        # shuffling list of names or sorting it
        if mixing_mode == ALL_TEXTS["mix_random_txt"]:
            random.shuffle(persons)
        elif mixing_mode == ALL_TEXTS["mix_alpha_txt"]:
            persons = sorted(list(persons))

        # calculation according to chosen split mode
        if split_mode == ALL_TEXTS["split_by_teams_txt"]:
            num_teams = split_mode_val
            num_members_by_team = num_persons // num_teams
            exceeding = num_persons % num_teams
        else:
            num_members_by_team = split_mode_val
            num_teams = num_persons // num_members_by_team
            exceeding = num_persons % num_members_by_team

        # assigning id's to empty team objects
        for i in range(num_teams):
            self.teams.append(team.Team(i+1))

        # populating teams
        for i in range(num_teams):
            current_members = persons[i*num_members_by_team:(i+1)*num_members_by_team]
            for this_member in current_members:
                self.teams[i].add(this_member)
            last_index = (i+1)*num_members_by_team

        # spread remainder if uneven teams
        if exceeding != 0:
            to_add = persons[last_index:]
            for i in range(exceeding):
                if len(to_add) != 0:
                    self.teams[i].add(to_add[0])
                    del to_add[0]

        # writing results to file
        data_to_write = []
        for i in range(len(self.teams)):
            data_to_write.append("\n-----------------------------------------------\n")
            data_to_write. append(ALL_TEXTS["team_txt"]+" #{}".format(self.teams[i].team_id) + ":\n")
            data_to_write.append("-----------------------------------------------\n")
            for cur_member in self.teams[i]:
                data_to_write.append(str(cur_member) + "\n")
        save_teams = open_a_file("teammaker/save/", "teams.txt")
        log_file = open_a_file("teammaker/save/my_teams", "teams_{}.txt".format(NOW))
        f = open(save_teams, "w+")
        log_f = open(log_file, "w+")
        for line in data_to_write:
            f.write(line)
            log_f.write(line)
        f.close()
        log_f.close()


class TeamMakerBoxLayout(BoxLayout):
    """Gui layout."""

    with open("teammaker/data/texts/{}/all_texts.json".format(LANG_CHOSEN)) as f2:
        json_data = f2.read()

    ALL_TEXTS = json.loads(json_data)
    header_image = "teammaker/images/teammaker.jpg"

    # Prompts
    num_people = ALL_TEXTS["num_people_txt"]
    split_team = ALL_TEXTS["split_team_txt"]
    choose = ALL_TEXTS["choose_txt"]
    split_by_team = ALL_TEXTS["split_by_teams_txt"]
    split_by_mem = ALL_TEXTS["split_by_members_txt"]
    enter_names = ALL_TEXTS["enter_names_txt"]
    mix_mode = ALL_TEXTS["mix_mode_txt"]
    mode1 = ALL_TEXTS["mode_random_txt"]
    mode2 = ALL_TEXTS["mode_alpha_txt"]
    mode3 = ALL_TEXTS["mode_as_is_txt"]
    make_teams_btn = ALL_TEXTS["make_teams_btn"]
    instructions = ALL_TEXTS["instructions_txt"]

    # randomizing colors
    num_people_color_r, num_people_color_g, num_people_color_b = random_choice_color()
    split_team_color_r, split_team_color_g, split_team_color_b = random_choice_color()
    mix_mode_color_r, mix_mode_color_g, mix_mode_color_b = random_choice_color()

    # methods
    def open_teams_popup(self):
        the_popup = TeamsPopup()
        the_popup.open()

    def open_names_popup(self):
        the_popup = NamesPopup()
        the_popup.open()

    def spinner_clicked(self, value):
        pass

    def split_mode(self, value):
        pass

    def open_instructions_popup(self):
        the_popup = InstructionsPopup()
        the_popup.open()


class TeamMakerGui(App):
    """Kivy builder"""

    title = "TeamMaker"
    def build(self):
        self.root = TeamMakerBoxLayout()
        return self.root