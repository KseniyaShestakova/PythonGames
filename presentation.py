import sys

import pygame

from internal_logics import *


def print_text_on_rect(screen, text, rect, font, color, rect_color):
    pygame.draw.rect(screen, rect_color, rect, width=0, border_radius=0, border_top_left_radius=(rect.y // 2),
                     border_top_right_radius=(rect.y // 2), border_bottom_left_radius=(rect.y // 2),
                     border_bottom_right_radius=(rect.y // 2))
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (rect.x + 5, rect.y + 5))
    pygame.display.flip()


def print_text(screen, text, font, color, rect_color, height):
    sz = font.size(text)  # (width, height)
    width = sz[0]
    screen_width = screen.get_size()[0]
    rect_height = sz[1]

    rect = pygame.Rect(int((screen_width - width) // 2), int(height), int(width) + 5, int(rect_height) + 5)
    print_text_on_rect(screen, text, rect, font, color, rect_color)


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
                         pygame.Rect(left - self.border_width,
                                     top + int(self.layer_height * (self.num_of_layers - (3 / 4))),
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

    def print_start_screen(self, base_font, comment_font, text_color, color, offset, base_step, comment_step):
        print_text(self.screen, 'Hello! ', base_font, text_color, color, offset)
        offset += base_step
        print_text(self.screen, 'Enter your name: ', base_font, text_color, color, offset)
        offset += base_step
        print_text(self.screen, 'It is needed for saving your progress. Name should be up to 8 characters ',
                   comment_font, text_color, color, offset)
        offset += comment_step
        return offset


    def show_size_options(self, base_font, base_step, offset, text_color, color, input_color):
        print_text(self.screen, 'Choose number of bottles: ', base_font, text_color, color, offset)
        offset += base_step

        size_options = 10
        start = 5
        rects_for_size = []
        width, height = base_font.size('10  ')
        height += 5
        step = width + 15
        left = (self.screen.get_size()[1] - (size_options // 2) * step) // 2

        for i in range(size_options // 2):
            rects_for_size.append(pygame.Rect(int(left + step * i), offset, width, height))

        offset += base_step
        for i in range(size_options // 2):
            rects_for_size.append(pygame.Rect(int(left + step * i), offset, width, height))

        for i in range(size_options):
            print_text_on_rect(self.screen, str(start + i), rects_for_size[i], base_font, text_color, input_color)

        return offset

    def check_size(self, event, base_font, base_step, offset, text_color, color, input_color, num_of_bottles):
        active_color = (218, 165, 32)
        if event.type != pygame.MOUSEBUTTONDOWN:
            return num_of_bottles
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            print(str(x) + ' ' + str(y))
            size_options, start = 10, 5
            width, height = base_font.size('10  ')
            step = width + 15
            height += 5
            left = (self.screen.get_size()[1] - (size_options // 2) * step) // 2
            if x < left or x > left + step * (size_options // 2):
                return num_of_bottles
            if y < offset + base_step or y > offset + 2 * base_step + height:
                return num_of_bottles

            left_offset = (x - left) // step

            if y > offset + height + base_step:
                ret = left_offset + size_options // 2
                self.show_size_options(base_font, base_step, offset, text_color, color, input_color)
                print_text_on_rect(self.screen, str(start + ret), pygame.Rect(int(left + step * left_offset),
                                                                              offset + 2 * base_step,
                                                                              width, height), base_font, text_color,
                                   active_color)
                return ret + start
            else:
                ret = left_offset
                self.show_size_options(base_font, base_step, offset, text_color, color, input_color)
                print_text_on_rect(self.screen, str(start + ret), pygame.Rect(int(left + step * left_offset),
                                                                              offset + base_step,
                                                                              width, height), base_font, text_color,
                                   active_color)
                return ret + start

    def start_screen(self):
        clock = pygame.time.Clock()
        # asks to enter your name and returns it
        background_color = (204, 204, 255)
        self.screen.fill(background_color)
        base_font = pygame.font.Font(None, 40)
        comment_font = pygame.font.Font(None, 20)

        text_color = (255, 255, 255)
        color = (135, 206, 250)

        offset = 10
        base_step = base_font.size('A')[1] + 10
        comment_step = comment_font.size('A')[1] + 10
        offset = self.print_start_screen(base_font, comment_font, text_color, color, offset, base_step, comment_step)

        # input text box
        input_rect = pygame.Rect(150, offset, 300, 37)
        input_color = (255, 255, 102)
        input_text = ''
        offset += base_step

        print_text_on_rect(self.screen, input_text, input_rect, base_font, text_color, input_color)

        active = False
        print_text_on_rect(self.screen, input_text, input_rect, base_font, text_color, (153, 51, 255))

        self.show_size_options(base_font, base_step, offset, text_color, color, input_color)

        confirm_rect = pygame.Rect(200, 400, 200, 35)
        print_text_on_rect(self.screen, 'Go on!', confirm_rect, base_font, text_color, input_color)

        pygame.display.flip()
        num_of_bottles = 8
        print(num_of_bottles)

        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                num_of_bottles = self.check_size(event, base_font, base_step, offset, text_color, color,
                                                 input_color, num_of_bottles)
                print(num_of_bottles)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if confirm_rect.collidepoint(pygame.mouse.get_pos()):
                        print(num_of_bottles)
                        return input_text, num_of_bottles

                    if input_rect.collidepoint(pygame.mouse.get_pos()):
                        active = True
                    else:
                        active = False

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

        left_offset = (x - self.left) // self.bottle_width
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
            x = self.left + self.bottle_width * (2 * num) - self.border_width
            y = self.top - 2 * self.border_width
        else:
            x = self.left + self.bottle_width * 2 * (num - self.width // (2 * self.bottle_width)) - self.border_width
            y = self.top + self.bottle_width + self.bottle_height - (2 * self.border_width)

        print(str(x) + ' ' + str(y))

        pygame.draw.rect(self.screen, self.background_color, pygame.Rect(x, y,
                                                                         self.bottle_width + 2 * self.border_width,
                                                                         self.bottle_height + 3 * self.border_width))
        self.draw_bottle(self.screen, self.bottle_list[num], x, y - self.bottle_width // 2)
        pygame.display.flip()

    def show_curr(self):
        self.screen.fill(self.background_color)
        self.draw_bottle_set(self.screen)
        pygame.display.flip()
