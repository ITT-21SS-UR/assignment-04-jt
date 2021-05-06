#!/usr/bin/python3

import math


class Improvement:

    def __init__(self, forms_list, radius):
        super().__init__()
        self.radius = radius
        self.distance = radius + 10
        self.new_pointer = ()
        self.forms_list = forms_list

    def filter(self, target_pos, curr_pos):
        middle = (target_pos[0] - self.radius / 2, target_pos[1] - self.radius / 2)
        offset = math.dist(middle, curr_pos)
        if offset <= self.distance:
            self.new_pointer = middle
        else:
            self.new_pointer = curr_pos
        return self.new_pointer
