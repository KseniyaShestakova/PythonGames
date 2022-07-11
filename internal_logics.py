import random
import drawing
import arcade
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
        return self.first_not_empty_layer - start

    def add_to_the_top(self, size=1):
        able_to_add = min(size, self.get_size_of_empty_space())
        for i in range(able_to_add):
            self.colors[self.first_not_empty_layer - i - 1] = self.get_top_color()
        return size - able_to_add

    def erase_from_the_top(self, size=1):
        able_to_erase = min(size, self.get_top_size())
        for i in range(able_to_erase):
            self.colors[self.first_not_empty_layer] = None
            self.first_not_empty_layer += 1


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
        _bottle_list = [Bottle(self.num_of_layers, color_list) for color_list in color_lists] + \
                       [Bottle(self.num_of_layers)] * num_empty
        self.bottle_list = _bottle_list


class State:
    # keeps information during the game
    initial_state = BottleSet()
    current_set = BottleSet()

def draw_bottle(surf, bottle, left, top, bottle_width, bottle_height, color_spectrum, background_color,
                border_color, border_width):
    colors = bottle.colors
    num_of_layers = bottle.num_of_layers
    layer_height = (bottle_height // (4 * num_of_layers)) * 4
    for layer in range(num_of_layers - 1):
        curr_color = background_color
        if colors[layer] is not None:
            curr_color = color_spectrum[colors[layer]]
        pygame.draw.rect(surf, curr_color, pygame.Rect(left, top + layer * layer_height, bottle_width, layer_height))

    curr_color = background_color
    if colors[num_of_layers - 1] is not None:
        curr_color = color_spectrum[colors[num_of_layers - 1]]

    pygame.draw.rect(surf, curr_color, pygame.Rect(left, top + (num_of_layers - 1) * layer_height,
                                                   bottle_width, layer_height // 4))
    pygame.draw.rect(surf, curr_color, pygame.Rect(left, top + (num_of_layers - 1) * layer_height + layer_height // 4,
                     bottle_width, 3 * (layer_height // 4)),
                     width=0, border_radius=0, border_top_left_radius=-1,
                     border_top_right_radius=-1, border_bottom_left_radius=bottle_width // 2,
                     border_bottom_right_radius=bottle_width // 2)

    pygame.draw.rect(surf, border_color, pygame.Rect(left - border_width, top - 2 * border_width,
                                                     border_width,
                                                     int(layer_height * (num_of_layers - (3/4))) + 2 * border_width))
    pygame.draw.rect(surf, border_color, pygame.Rect(left + bottle_width, top - 2 * border_width,
                                                     border_width,
                                                     int(layer_height * (num_of_layers - (3/4))) + 2 * border_width))

    pygame.draw.rect(surf, border_color, pygame.Rect(left - border_width, top + int(layer_height * (num_of_layers - (3/4))),
                     bottle_width + 2 * border_width, 3 * (layer_height // 4)),
                     width=border_width, border_radius=0, border_top_left_radius=-1,
                     border_top_right_radius=-1, border_bottom_left_radius=bottle_width // 2,
                     border_bottom_right_radius=bottle_width // 2)
    pygame.draw.rect(surf, curr_color, pygame.Rect(left, top + int(layer_height * (num_of_layers - (3/4))),
                                                   bottle_width, border_width))


def draw_bottle_set(surf, color_spectrum, bottle_set=BottleSet(),
                    width=600, height=600, border_width=2, border_color=(96, 96, 96), background_color=(204, 204, 255)):
    bottle_list = bottle_set.get_list()
    num_of_bottles = bottle_set.get_num_of_bottles()
    columns = num_of_bottles + 2

    bottle_width = (width // (4 * columns)) * 4
    bottle_height = ((height - 4 * bottle_width) // 8) * 4

    left = bottle_width
    top = 2 * bottle_width

    first_portion = width // (2 * bottle_width)

    for cnt in range(first_portion):
        draw_bottle(surf, bottle_list[cnt], left + 2 * bottle_width * cnt, top, bottle_width, bottle_height,
                    color_spectrum, background_color, border_color, border_width)

    top += bottle_height + bottle_width

    for cnt in range(first_portion, num_of_bottles):
        draw_bottle(surf, bottle_list[cnt], left + 2 * bottle_width * (cnt - first_portion) , top, bottle_width, bottle_height,
                    color_spectrum, background_color, border_color, border_width)




