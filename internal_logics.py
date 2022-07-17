import random
import pygame
import time


class Bottle:
    colors = []
    num_of_layers = 0
    first_not_empty_layer = num_of_layers

    def __init__(self, _num_of_layers=4, color_list=None):
        self.num_of_layers = _num_of_layers
        if color_list is not None:
            self.colors = color_list
            self.first_not_empty_layer = 0
            while (self.first_not_empty_layer < self.num_of_layers) and (self.colors[self.first_not_empty_layer] is None):
                self.first_not_empty_layer += 1
        else:
            self.colors = [None] * self.num_of_layers
            self.first_not_empty_layer = self.num_of_layers

    def get_top_color(self):
        if self.first_not_empty_layer == self.num_of_layers:
            return None
        return self.colors[self.first_not_empty_layer]

    def get_size_of_empty_space(self):
        return self.first_not_empty_layer

    def get_top_size(self):
        if self.first_not_empty_layer == self.num_of_layers:
            return 0
        start = self.first_not_empty_layer
        while start < self.num_of_layers and self.colors[start] == self.get_top_color():
            start += 1
        return start - self.first_not_empty_layer

    def add_to_the_top(self, size, color):
        able_to_add = min(size, self.get_size_of_empty_space())
        for i in range(able_to_add):
            self.colors[self.first_not_empty_layer - i - 1] = color
        self.first_not_empty_layer -= able_to_add
        return able_to_add

    def erase_from_the_top(self, size=1):
        able_to_erase = min(size, self.get_top_size())
        for i in range(able_to_erase):
            self.colors[self.first_not_empty_layer] = None
            self.first_not_empty_layer += 1
            self.first_not_empty_layer = min(self.first_not_empty_layer, self.num_of_layers)

    def is_filled(self):
        return self.get_top_size() == self.num_of_layers


def are_compatible(first_bottle, second_bottle):
    print(first_bottle.get_top_color())
    print(second_bottle.get_top_color())
    print(second_bottle.get_size_of_empty_space())
    return ((first_bottle.get_top_color() == second_bottle.get_top_color()) and
            second_bottle.get_size_of_empty_space() >= 1) or \
           (second_bottle.get_size_of_empty_space() == second_bottle.num_of_layers)


class BottleSet:
    bottle_list = []
    num_of_bottles = 0
    num_of_layers = 0

    def get_list(self):
        return self.bottle_list

    def get_num_of_bottles(self):
        return self.num_of_bottles

    def get_num_of_layers(self):
        return self.num_of_layers

    def __init__(self, _num_of_bottles=5, _num_of_layers=4, _bottle_list=None):
        self.num_of_bottles = _num_of_bottles
        self.num_of_layers = _num_of_layers
        if _bottle_list is not None:
            self.bottle_list = _bottle_list
        else:
            self.bottle_list = [Bottle(self.num_of_layers)] * self.num_of_bottles

    def random_filling(self, num_empty=None):
        if num_empty is None:
            num_empty = 2
        num_filled = self.num_of_bottles - num_empty

        color_lists = []
        for i in range(num_filled):
            color_lists.append([])
        color_spectrum = [i for i in range(num_filled)] * self.num_of_layers
        for curr in range(num_filled):
            for i in range(self.num_of_layers):
                rand_color = random.randint(0, len(color_spectrum) - 1)
                color_lists[curr].append(color_spectrum[rand_color])
                color_spectrum.pop(rand_color)
        _bottle_list = [Bottle(self.num_of_layers, color_list) for color_list in color_lists]
        for i in range(num_empty):
            _bottle_list.append(Bottle(self.num_of_layers))
        self.bottle_list = _bottle_list

    def are_compatible(self, first, second):
        if first >= len(self.bottle_list) or second >= len(self.bottle_list) or first == second:
            return False
        return are_compatible(self.bottle_list[first], self.bottle_list[second])

    def count_filled(self):
        ret = 0
        for bottle in self.bottle_list:
            if bottle.get_top_size() == bottle.num_of_layers:
                ret += 1

        return ret
