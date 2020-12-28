import random

class Colormaker:
    """
    This class generates random rgba colors with conversions for kivy range (0-1).

    Attributes:
        num (int): The number of colors to generate.
        low (int): Lower range of rgb values going from 0 to 255.
        high (int): Higher range of rgb values going from 0 to 255.
    """

    def __init__(self, num, low, high):
        self.num_colors = num
        self.low_range = low
        self.high_range = high
        self.colors = []
        self.colors_storage = []
        self.make_colors()

    def make_colors(self):
        """
        Produces the random colors according to the range specified, makes the necessary
        conversions and stores the values in a list.
        """

        for i in range(4 * self.num_colors):
            this_color = random.randint(self.low_range, self.high_range)
            while this_color in self.colors:
                this_color = random.randint(self.low_range, self.high_range)
            self.colors.append(round((this_color / 255), 3))
        for i in range(self.num_colors):
            self.colors_storage.append(self.colors[:4])
            self.colors = self.colors[4:]

    def __len__(self):
        return len(self.colors_storage)

    def __getitem__(self, i):
        return self.colors_storage[i]
