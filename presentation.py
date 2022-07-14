import sys

from internal_logics import *


def print_text_on_rect(screen, text, rect, font, color, rect_color):
    pygame.draw.rect(screen, rect_color, rect)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (rect.x + 5, rect.y + 5))


class Representor:
    bottle_list = []
    num_of_bottles = 0
    columns = 0

    width = 0  # width of the screen
    height = 0  # height of the screen

    bottle_width = 0
    bottle_height = 0

    num_of_layers = 0
    layer_height = 0

    rects_to_bottles = dict()

    def reset(self, _width, _height, bottle_set=BottleSet()):
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

        first_portion = self.width // (2 * self.bottle_width)
        left = self.bottle_width
        top = 2 * self.bottle_width

        for cnt in range(first_portion):
            self.rects_to_bottles[cnt] = pygame.Rect(left + 2 * self.bottle_width * cnt, top,
                                                     self.bottle_width, self.bottle_height)

        top += self.bottle_height + self.bottle_width

        for cnt in range(first_portion, self.num_of_bottles):
            self.rects_to_bottles[cnt] = pygame.Rect(left + 2 * self.bottle_width * (cnt - first_portion), top,
                                                     self.bottle_width, self.bottle_height)

    def __init__(self, _width, _height, bottle_set=BottleSet()):
        self.reset(_width, _height, bottle_set)

    def draw_bottle(self, surf, bottle, left, top, color_spectrum, background_color,
                    border_color, border_width):
        colors = bottle.colors

        for layer in range(self.num_of_layers - 1):
            curr_color = background_color
            if colors[layer] is not None:
                curr_color = color_spectrum[colors[layer]]
            pygame.draw.rect(surf, curr_color, pygame.Rect(left, top + layer * self.layer_height,
                                                           self.bottle_width, self.layer_height))

        curr_color = background_color
        if colors[self.num_of_layers - 1] is not None:
            curr_color = color_spectrum[colors[self.num_of_layers - 1]]

        pygame.draw.rect(surf, curr_color, pygame.Rect(left, top + (self.num_of_layers - 1) * self.layer_height,
                                                       self.bottle_width, self.layer_height // 4))
        pygame.draw.rect(surf, curr_color,
                         pygame.Rect(left, top + (self.num_of_layers - 1) * self.layer_height + self.layer_height // 4,
                                     self.bottle_width, 3 * (self.layer_height // 4)),
                         width=0, border_radius=0, border_top_left_radius=-1,
                         border_top_right_radius=-1, border_bottom_left_radius=self.bottle_width // 2,
                         border_bottom_right_radius=self.bottle_width // 2)

        pygame.draw.rect(surf, border_color, pygame.Rect(left - border_width, top - 2 * border_width,
                                                         border_width,
                                                         int(self.layer_height * (
                                                                 self.num_of_layers - (3 / 4))) + 2 * border_width))
        pygame.draw.rect(surf, border_color, pygame.Rect(left + self.bottle_width, top - 2 * border_width,
                                                         border_width,
                                                         int(self.layer_height * (
                                                                 self.num_of_layers - (3 / 4))) + 2 * border_width))

        pygame.draw.rect(surf, border_color,
                         pygame.Rect(left - border_width, top + int(self.layer_height * (self.num_of_layers - (3 / 4))),
                                     self.bottle_width + 2 * border_width, 3 * (self.layer_height // 4)),
                         width=border_width, border_radius=0, border_top_left_radius=-1,
                         border_top_right_radius=-1, border_bottom_left_radius=self.bottle_width // 2,
                         border_bottom_right_radius=self.bottle_width // 2)
        pygame.draw.rect(surf, curr_color,
                         pygame.Rect(left, top + int(self.layer_height * (self.num_of_layers - (3 / 4))),
                                     self.bottle_width, border_width))

    def draw_bottle_set(self, surf, color_spectrum, bottle_set=BottleSet(),
                        border_width=2, border_color=(96, 96, 96), background_color=(204, 204, 255)):
        left = self.bottle_width
        top = 2 * self.bottle_width

        first_portion = self.width // (2 * self.bottle_width)

        for cnt in range(first_portion):
            self.draw_bottle(surf, self.bottle_list[cnt], left + 2 * self.bottle_width * cnt, top,
                             color_spectrum, background_color, border_color, border_width)

        top += self.bottle_height + self.bottle_width

        for cnt in range(first_portion, self.num_of_bottles):
            self.draw_bottle(surf, self.bottle_list[cnt], left + 2 * self.bottle_width * (cnt - first_portion), top,
                             color_spectrum, background_color, border_color, border_width)

    def start_screen(self, screen):
        clock = pygame.time.Clock()
        # asks to enter your name and returns it
        background_color = (204, 204, 255)
        screen.fill(background_color)
        base_font = pygame.font.Font(None, 32)
        comment_font = pygame.font.Font(None, 16)

        hello_rect = pygame.Rect(10, 10, 100, 32)
        information_rect = pygame.Rect(10, 42, 200, 32)
        comments_rect = pygame.Rect(10, 74, 400, 16)

        text_color = (255, 255, 255)
        color = (135, 206, 250)
        print_text_on_rect(screen, 'Hello!', hello_rect, base_font, text_color, color)
        print_text_on_rect(screen, 'Enter your name:', information_rect, base_font, text_color, color)
        print_text_on_rect(screen, 'It is needed for saving your progress. Name should be up to 8 characters',
                           comments_rect, comment_font, text_color, color)

        pygame.display.flip()

        # input text box
        input_rect = pygame.Rect(10, 90, 300, 32)
        input_color = (255, 255, 102)
        input_text = ''

        pygame.draw.rect(screen, input_color, input_rect)

        active = False

        confirm_rect = pygame.Rect(10, 140, 200, 32)
        print_text_on_rect(screen, 'Confirm', confirm_rect, base_font, text_color, color)
        print_text_on_rect(screen, input_text, input_rect, base_font, text_color, (153, 51, 255))
        pygame.display.flip()
        confirmed = False

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
                        pygame.quit()
                        sys.exit()

                if not active:
                    continue

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

                print_text_on_rect(screen, input_text, input_rect, base_font, text_color, (153, 51, 255))
                pygame.display.flip()

                clock.tick(60)
