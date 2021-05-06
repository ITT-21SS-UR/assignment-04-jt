#!/usr/bin/python3

import math


class Improvement:

    def __init__(self, forms_list, radius):
        super().__init__()
        self.distance = radius + 10
        self.new_pointer = ()
        self.forms_list = forms_list

    def filter(self, target_pos, curr_pos):
        offset = math.dist(target_pos, curr_pos)
        if offset <= self.distance:
            self.new_pointer = target_pos
        else:
            self.new_pointer = curr_pos
        return self.new_pointer
