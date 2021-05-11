#!/usr/bin/python3

import math

# all work was contributed evenly between the two group members

""" To improve the pointing via mouse we implemented this method.
For this the function filter() gets the position of the target and the current cursor position.
The coordinates of the target are in their right down corner. Because our targets are always circles, 
we calculate first the middle of the circle-target.
Then we calculate the distance between the current cursor position and the middle of the target.
If this offset is smaller than or equal to the distance we defined (diameter of the target + 10) the cursor 
gets "magnetically" pulled to the center of the target by setting its coordinates to the coordinates of the 
middle of the target. These are then returned to ExperimentTest. If the offset is bigger than the distance, 
the current position of the cursor gets returned.
"""


class Improvement:

    def __init__(self, forms_list, diameter):
        super().__init__()
        self.radius = diameter / 2
        self.distance = diameter + 10
        self.new_pointer = ()
        self.forms_list = forms_list

    def filter(self, target_pos, curr_pos):
        middle = (target_pos[0] - self.radius, target_pos[1] - self.radius)
        offset = math.dist(middle, curr_pos)
        if offset <= self.distance:
            self.new_pointer = middle
        else:
            self.new_pointer = curr_pos
        return self.new_pointer
