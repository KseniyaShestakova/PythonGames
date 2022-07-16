import sys

import pygame

from internal_logics import *


def print_text_on_rect(screen, text, rect, font, color, rect_color):
    pygame.draw.rect(screen, rect_color, rect)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (rect.x + 5, rect.y + 5))


class Representor:
    screen = None
    background_color = (204, 204, 255)
    color_spectrum = None
    border_color = (96, 96, 96)
    border_width = 2
    bottle_list = []
    num_of_bottles = 0
    columns = 0

    width = 0  # width of the screen
    height = 0  # height of the screen

    bottle_width = 0
    bottle_height = 0

    num_of_layers = 0
    layer_height = 0

    left = 0
    top = 0

    def reset(self, bottle_set=BottleSet(), _width=600, _height=600):
        self.width = _width
        self.height = _height
        self.bottle_list = bottle_set.get_list()
        self.num_of_bottles = bottle_set.get_num_of_bottles()
        self.columns = self.num_of_bottles + 2

        self.bottle_width = (self.width // (4 * self.columns)) * 4
        self.bottle_height = ((self.height - 4 * self.bottle_width) // 8) * 4

        if len(self.bottle_list):
            self.num_of_layers = self.bottle_list[0].num_of_layers
        else:
            self.num_of_layers = 4

        self.layer_height = (self.bottle_height // (4 * self.num_of_layers)) * 4

        self.left = self.bottle_width
        self.top = 2 * self.bottle_width

    def __init__(self, _screen, _width=600, _height=600, _color_spectrum=((0, 0, 205), (255, 140, 0), (135, 206, 235),
                                                                  (0, 255, 255), (250, 128, 114),
                                                                  (154, 205, 50), (139, 0, 139), (255, 215, 0)),
                 _border_color=(96, 96, 96), _border_width=2,
                 _background_color=(204, 204, 255), bottle_set=BottleSet()):
        self.screen = _screen
        self.background_color = _background_color
        self.border_color = _border_color
        self.bottle_width = _border_width
        self.color_spectrum = _color_spectrum
        self.reset(bottle_set, _width, _height)

    def draw_bottle(self, surf, bottle, left, top):
        colors = bottle.colors

        for layer in range(self.num_of_layers - 1):
            curr_color = self.background_color
            if colors[layer] is not None:
                curr_color = self.color_spectrum[colors[layer]]
            pygame.draw.rect(surf, curr_color, pygame.Rect(left, top + layer * self.layer_height,
                                                           self.bottle_width, self.layer_height))

        curr_color = self.background_color
        if colors[self.num_of_layers - 1] is not None:
            curr_color = self.color_spectrum[colors[self.num_of_layers - 1]]

        pygame.draw.rect(surf, curr_color, pygame.Rect(left, top + (self.num_of_layers - 1) * self.layer_height,
                                                       self.bottle_width, self.layer_height // 4))
        pygame.draw.rect(surf, curr_color,
                         pygame.Rect(left, top + (self.num_of_layers - 1) * self.layer_height + self.layer_height // 4,
                                     self.bottle_width, 3 * (self.layer_height // 4)),
                         width=0, border_radius=0, border_top_left_radius=-1,
                         border_top_right_radius=-1, border_bottom_left_radius=self.bottle_width // 2,
                         border_bottom_right_radius=self.bottle_width // 2)

        pygame.draw.rect(surf, self.border_color, pygame.Rect(left - self.border_width, top - 2 * self.border_width,
                                                              self.border_width,
                                                              int(self.layer_height * (
                                                                      self.num_of_layers - (
                                                                          3 / 4))) + 2 * self.border_width))
        pygame.draw.rect(surf, self.border_color, pygame.Rect(left + self.bottle_width, top - 2 * self.border_width,
                                                              self.border_width,
                                                              int(self.layer_height * (
                                                                      self.num_of_layers - (
                                                                          3 / 4))) + 2 * self.border_width))

        pygame.draw.rect(surf, self.border_color,
                         pygame.Rect(left - self.border_width, top + int(self.layer_height * (self.num_of_layers - (3 / 4))),
                                     self.bottle_width + 2 * self.border_width, 3 * (self.layer_height // 4)),
                         width=self.border_width, border_radius=0, border_top_left_radius=-1,
                         border_top_right_radius=-1, border_bottom_left_radius=self.bottle_width // 2,
                         border_bottom_right_radius=self.bottle_width // 2)
        pygame.draw.rect(surf, curr_color,
                         pygame.Rect(left, top + int(self.layer_height * (self.num_of_layers - (3 / 4))),
                                     self.bottle_width, self.border_width))

    def draw_bottle_set(self, surf):
        first_portion = self.width // (2 * self.bottle_width)

        for cnt in range(first_portion):
            self.draw_bottle(surf, self.bottle_list[cnt], self.left + 2 * self.bottle_width * cnt, self.top)

        self.top += self.bottle_height + self.bottle_width

        for cnt in range(first_portion, self.num_of_bottles):
            self.draw_bottle(surf, self.bottle_list[cnt], self.left + 2 * self.bottle_width * (cnt - first_portion),
                             self.top)

        self.top -= self.bottle_height + self.bottle_width

    def start_screen(self):
        clock = pygame.time.Clock()
        # asks to enter your name and returns it
        background_color = (204, 204, 255)
        self.screen.fill(background_color)
        base_font = pygame.font.Font(None, 32)
        comment_font = pygame.font.Font(None, 16)

        hello_rect = pygame.Rect(10, 10, 100, 32)
        information_rect = pygame.Rect(10, 42, 200, 32)
        comments_rect = pygame.Rect(10, 74, 400, 16)

        text_color = (255, 255, 255)
        color = (135, 206, 250)
        print_text_on_rect(self.screen, 'Hello!', hello_rect, base_font, text_color, color)
        print_text_on_rect(self.screen, 'Enter your name:', information_rect, base_font, text_color, color)
        print_text_on_rect(self.screen, 'It is needed for saving your progress. Name should be up to 8 characters',
                           comments_rect, comment_font, text_color, color)

        pygame.display.flip()

        # input text box
        input_rect = pygame.Rect(10, 90, 300, 32)
        input_color = (255, 255, 102)
        input_text = ''

        pygame.draw.rect(self.screen, input_color, input_rect)

        active = False

        confirm_rect = pygame.Rect(10, 140, 200, 32)
        print_text_on_rect(self.screen, 'Confirm', confirm_rect, base_font, text_color, color)
        print_text_on_rect(self.screen, input_text, input_rect, base_font, text_color, (153, 51, 255))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                print("here")
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(pygame.mouse.get_pos()):
                        active = True
                    else:
                        active = False
                    if confirm_rect.collidepoint(pygame.mouse.get_pos()):
                        print("confirmed")
                        return input_text

                if not active:
                    continue

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

                print_text_on_rect(self.screen, input_text, input_rect, base_font, text_color, (153, 51, 255))
                pygame.display.flip()

                clock.tick(60)

    def collide_with(self, pos):
        x = pos[0]
        y = pos[1]
        # return the number of bottle to which this point belongs
        if x < self.left or y < self.top:
            return None

        left_offset = (x - self.left) // self.width
        if left_offset % 2 == 1:
            return None

        left_offset //= 2

        if y - self.top <= self.bottle_height:
            return left_offset

        y -= (self.top + self.bottle_height)

        if y < self.bottle_width or y > self.bottle_width + self.bottle_height:
            return None

        return left_offset + self.width // (2 * self.bottle_width)

    def lift(self, num):
        # lifts the bottle with number num
        if num < self.width // (2 * self.bottle_width):
            x = self.top + self.bottle_width * 2 * num - self.border_width
            y = self.left - 2 * self.border_width
        else:
            x = self.top + self.bottle_width * 2 * (num - self.width // (2 * self.bottle_width)) - self.border_width
            y = self.top + self.bottle_width + self.bottle_height - 2 * self.border_width

        pygame.draw.rect(self.screen, self.background_color, pygame.Rect(x, y,
                                                                         self.bottle_width + 2 * self.border_width,
                                                                         self.bottle_height + 3 * self.border_width))
        self.draw_bottle(self.screen, self.bottle_list[num], x, y - self.bottle_width // 2)

    def show_curr(self):
        self.screen.fill(self.background_color)
        self.draw_bottle_set(self.screen)
        pygame.display.flip()
