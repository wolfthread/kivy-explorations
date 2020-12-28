import config
import kivy
import json
kivy.require("1.10.1")

from kivy.core.window import Window
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.popup import Popup
from kivy.properties import ListProperty, BooleanProperty
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock

"""
This module creates the Course Tracker application that generates a course study session according to preset
order or using a random mode. A settings panel is accessible for modyfing the different courses settings.

"""
def on_save_button():
    """Self-dismiss popup showing 'saved' text"""
    the_popup = ShowSavedPopup()
    the_popup.open()


class ShowSavedPopup(Popup):
    """Popup class showing a slight "saved!" message when user saves data."""

    def __init__(self, **kwargs):
        super(ShowSavedPopup, self).__init__(**kwargs)
        Clock.schedule_once(self.dismiss_popup, 0.5)

    def dismiss_popup(self, dt):
        self.dismiss()


class PopupColor(Popup):
    """Popup class opening a color picker wheel and draggable setting."""


    def on_press_dismiss(self, colorpicker, *args):
        color = ListProperty()
        color = colorpicker.color
        self.dismiss()
        app = App.get_running_app()
        app.root.ids.color_button.background_color = color


class PopupConfirmDelete(Popup):
    """Popup class deleting a course through the config file after confirmation by user."""


    def on_press_dismiss(self, answerbtn, *args):
        if answerbtn:
            app = App.get_running_app()
            course_to_delete = app.root.ids.course_choice.text
            new_menu = []
            config.delete(MyPanel.order, MyPanel.parameters, course_to_delete)
            for item in MyPanel.parameters["Courses"]:
                new_menu.append(item['Name'])
            app.root.ids.course_choice.values = new_menu + ["(add a course)"]
            app.root.ids.course_choice.text = ""
#            app.root.ids.color_button.background_color = [1,1,1,1]
#            app.root.ids.order.value = 0
        self.dismiss()



class MyPanel(TabbedPanel):
    """Main Panel containing all functions for all tabs."""


    random_mode = BooleanProperty()
    order, by_courses, courses, bg_cust_colors_conv, parameters, random_mode = config.initialize()
    add = False
    num_courses = len(courses)
    text = order[0] if len(order) else "No Courses Added"
    list_of_courses = list(by_courses.keys())
    assigned_color = bg_cust_colors_conv
    order_value = by_courses[text][2] if len(by_courses) else 0
    frequency_value = by_courses[text][1] if len(by_courses) else 0
    instructions = """
    FIRST SETUP:
    You can edit the template that has 4 courses included.
    For this, click on the settings tab and edit the name.
    Choose the color you want to assign to the course.
    Use random mode or set the order you want.
    Click on the SAVE button.

    ADD A COURSE:
    If you want to add a course, simply choose this option from the course dropdown.
    You can then edit the course name and set the color and order accordingly.

    REMOVE A COURSE:
    If you want to remove a course, simply click on REMOVE.
    You will be prompted to confirm before deletion.
    """

    def assign_color(self, course):
        """Function assigning a color to the course sent in parameter"""
        assigned_color = self.by_courses[course][0]

    def change_color(self):
        """Popup to change the color"""
        popup = PopupColor()
        popup_color = ColorPicker()
        new_color = popup.open()

    def confirm_delete(self):
        """Popup to confirm deletion"""
        popup = PopupConfirmDelete()
        popup.open()

    def confirm_exit(self):
        """Popup confirming exit"""
        popup = PopupConfirmExit()
        popup.open()

    def completion(self, ans):
        """Function confirming the completion of the session, exiting afterwards.

        Args:
            ans (bool): Confirmation if deletion or not.

        """

        if ans :
            config.save(self.by_courses, self.order, self.parameters, True)
        else:
            config.save(self.by_courses, self.order, self.parameters, False)
        exit()

    def save_changes(self):
        """Function saving changes set in the setting tab, through the config.py file.
        Todo:
            * Needs major cleanup
            * Add frequency functionality

        """


        app = App.get_running_app()
        current_course = app.root.ids.course_choice.text
        edit_name = app.root.ids.name.text
        new_order = app.root.ids.order.value
#        new_frequency = app.root.ids.frequency.value
        new_color = app.root.ids.color_button.background_color
        if current_course in self.by_courses:
            for item in self.by_courses:
                if item == current_course:
                    self.by_courses[item][0] = new_color
    #                by_courses[item][1] = new_frequency
                    self.by_courses[item][2] = new_order
            for item in self.parameters["Courses"]:
                if item["Name"] == current_course:
                    item["Color"] = new_color
    #                item["Frequency"] = new_frequency
                    item["Order"] = new_order
                    if edit_name != current_course:
                        item["Name"] = edit_name
                        self.by_courses[edit_name] = self.by_courses.pop(current_course)
                        if current_course in self.order:
                            self.order[self.order.index(current_course)] = edit_name
        else:
            self.by_courses[edit_name] = [new_color, 1, new_order]
            self.order.append(edit_name)
            self.parameters["Courses"].append({"Name": edit_name, "Color": new_color, "Frequency": 1, "Order": new_order})
        app.root.ids.course_choice.values = list(self.by_courses.keys()) +  ["(add a course)"]
        config.save(self.by_courses, self.order, self.parameters, False)
        on_save_button()

    def change_random_mode(self, random_mode):
        """Saving only 1 parameter"""
        config.save_only_parameter("Random", random_mode)

    def course_choice(self, ans):
        """Function assigning values in gui for a selection in spinner.

        Args:
            ans (string): Course name.

        """
        assigned_color = ListProperty()
        self.text = self.order[0]
        assigned_color = [1,1,1,1] if ans == '' else self.by_courses[ans][0]
        app = App.get_running_app()
        app.root.ids.color_button.background_color = assigned_color
        app.root.ids.order.value =0 if ans == '' else self.by_courses[ans][2]
#        app.root.ids.frequency.value = by_courses[ans][1]

    def add_course(self):
        self.add = True

class courseTracker(App):
    """Main app class, with window set for an optimal settings view."""

    Window.size = 600, 400
    def build(self):
        return MyPanel()


if __name__ == '__main__':
    courseTracker().run()
