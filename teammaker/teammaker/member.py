class Member:
    """
    This is a class to create a member of a team.

    Attributes:
        first_name (str): The first name of the person. Optional. If omitted, empty string used.
        last_name (str): The last name of the person. Optional. If omitted, empty string used.
    """

    def __init__(self, first_name = '', last_name = ''):
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        """Method returning a string of the first and last name."""

        return "{} {}".format(self.first_name, self.last_name)

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        """Comparison used for sorting the team members."""

        return self.first_name < other.first_name