import json
import random

from kivy.properties import ListProperty

"""
This module contains functions necessary to configure each Course Tracker session using a JSON file.

"""

# class methods

def set_order(par):
    """Function setting the order according to the presetting of the user

    Args:
        par (list): A list of dictionaries including all the parameters.

    Returns:
        list: Courses names set in order.

    """
    number_of_course = len(par["Courses"]) # just needing the courses parameter
    new_order = [None for x in range(number_of_course)]
    all_courses = []
    for item in par["Courses"]:
        new_order[item["Order"]-1] = item["Name"]
        all_courses.append(item["Name"]) # safety in case user does not enter correct order
    if None in new_order:
        new_order = all_courses
    return new_order

def save_only_parameter(par, new_value, second_par = None):
    """Function used to save only one parameter to JSON format.

    Args:
        par (string):  The parameter that represents a key of the stored JSON file.
        new_value (int, string or list): The new value to be set in parameters.
        second_par (string): If passed in parameters, this would be a key for one of the courses dictionary.

    """

    with open("config.json") as config_f:
        json_data = config_f.read()
    changed_parameters = json.loads(json_data)
    if not second_par:
        changed_parameters[par] = new_value
    else:
        print("will save other stuff... ", new_value)
    with open('config.json', 'w') as json_file:
        json.dump(changed_parameters, json_file)


def delete(order, parameters, course_to_delete):
    """Function used to delete a course from the stored JSON file.

    Args:
        order (list): The list of courses in preset order.
        parameters (dict): A list of dictionaries including all the parameters.
        course_to_delete (string): The name of the course to be deleted.

    """
    if course_to_delete in order:
        order.remove(course_to_delete)
        if not len(order):
            order.append("No Courses Added")
    for item in parameters["Courses"]:
        if item["Name"] == course_to_delete:
            parameters["Courses"].remove(item)
    parameters["Order"] = order
    with open('config.json', 'w') as json_file:
        json.dump(parameters, json_file)


def save(by_courses, order, parameters, done):
    """Function saving all the parameters from the current session to the stored JSON file.

    Args:
        by_courses (dict): A dictionary of courses parameters with courses names as keys.
        order (list): The list of courses in preset order.
        parameters (dict): A list of dictionaries including all the parameters.
        done (bool): Representing if the session is completed or not.

    """

    with open("config.json") as config_f:
        json_data = config_f.read()
    changed_parameters = json.loads(json_data)
    parameters["Random"] = True if changed_parameters["Random"] else False
    course_names = list(by_courses.keys())
    old_order = course_names
    if len(order) == 1 and done:
        if parameters["Random"]:
            random.shuffle(old_order)
        else:
            old_order = set_order(parameters)
        parameters["Order"] = old_order
    elif done:
        del parameters["Order"][0] # removing the course from the order as session is completed
    elif not done:
        parameters["Order"] = order
    with open('config.json', 'w') as json_file:
        json.dump(parameters, json_file)

def initialize():
    """Function initializing all the necessary parameters to start the course tracker app.

    Returns:
        tuple: Containing a list, a dict, a list of dicts, a ListProperty, a dict, a BooleanProperty

    """

    with open("config.json") as config_f:
        json_data = config_f.read()
    parameters = json.loads(json_data)
    order = []
    by_courses = {}
    courses = []
    color_set = [1,1,1,1]
    random_mode = True if parameters['Random'] else False
    if len(parameters["Courses"]) >=1:
        courses = [x for x in parameters['Courses']]
        by_courses = {}
        for item in courses:
            by_courses[item['Name']] = [item['Color'], item['Frequency'], item['Order']]
        order = parameters["Order"]
        cust_colors = by_courses[order[0]][0]
        color_set = ListProperty(cust_colors)
    return (order, by_courses, courses, color_set, parameters, random_mode) # list, dict, list of dicts, ListProperty, dict, BooleanProperty
