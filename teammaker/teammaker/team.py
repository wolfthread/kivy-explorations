class Team:
    """
    This is a class to create a team.

    Attributes:
        team (list): An empty list at creation to store team members.
        team_id (int): A number assigned to the team to identify it.
    """

    def __init__(self, num):
        self.team = []
        self.team_id = num

    def add(self, member):
        """
        The function adds a member to the team.

        Parameters:
            member (Member object): The member to be added to the team.
        """

        self.team.append(member)

    def remove(self, member):
        """
        The function removes a member from the team.

        Parameters:
            member (Member object): The member to be removed from the team.
        """

        self.team.remove(member)

    def __getitem__(self, i):
        """
        Obtain a member from the team according to its position in the team.

        Parameters:
            i (int): Position of the team member.

        Returns:
            Member: A Member object at position i.
        """

        return self.team[i]

    def __str__(self):
        """
        Prints the complete team as a string.

        Returns:
            s: String containing the team members.
        """
        s = ''
        for item in self.team:
            s += str(item)
        return s

    def __repr__(self):
        return str(self)