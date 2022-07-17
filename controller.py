from presentation import *

FUCHSIA = (204, 0, 102)
LILAC = (139, 0, 139)
LIGHTSKYBLUE = (135, 206, 250)
CORNFLOWERBLUE = (0, 0, 205)  # MEDIUMBLUE
DARKBLUE = (0, 0, 139)
LIGHTCYAN = (40, 255, 255)
GOLDENROD = (255, 255, 51)
LIGHTSALMON = (178, 34, 34)
SPRINGGREEN = (0, 255, 127)
ORANGE = (210, 105, 30)
ORCHID = (218, 112, 214)
SANDYBROWN = (244, 164, 96)
ROSYBROWN = (188, 143, 143)
GREEN = (0, 128, 0)


class Controller:
    name = ''
    coins = 0
    num_of_filled = 0
    need_to_be_filled = 0
    plus = 0

    initial = BottleSet()
    current = BottleSet()
    previous = BottleSet()
    num_of_bottles = initial.num_of_bottles
    num_empty = 2
    representor = None

    def __init__(self, _bottle_set=BottleSet(), _width=600, _height=600,
                 _color_spectrum=( FUCHSIA, LILAC, LIGHTSKYBLUE, CORNFLOWERBLUE, DARKBLUE, LIGHTCYAN,
                                GOLDENROD, LIGHTSALMON, SPRINGGREEN, ORANGE, ORCHID, SANDYBROWN,
                                ROSYBROWN, GREEN),
                 _border_color=(96, 96, 96), _border_width=2,
                 _background_color=(204, 204, 255)):
        pygame.init()
        _screen = pygame.display.set_mode((_width, _height))
        self.representor = Representor(_screen, _width, _height, _color_spectrum, _border_color, _border_width,
                                       _background_color, _bottle_set)
        self.initial = _bottle_set
        self.current = _bottle_set
        self.previous = _bottle_set

    def random_filling(self, _num_of_bottles, num_empty=2):
        self.num_of_bottles = _num_of_bottles
        self.initial = BottleSet(_num_of_bottles)
        self.initial.random_filling(num_empty)
        self.current = self.initial
        self.previous = self.initial
        self.num_of_filled = self.current.count_filled()
        self.need_to_be_filled = self.num_of_bottles - num_empty

    def restart(self):
        self.current = self.initial
        self.previous = self.initial

    def step_back(self):
        # can be applied once
        self.current = self.previous

    def get_bottle(self, num):
        # may be returns copy
        return self.current.bottle_list[num]

    def add_to(self, num, size, color):
        return self.current.bottle_list[num].add_to_the_top(size, color)

    def erase_from(self, num, size=1):
        self.current.bottle_list[num].erase_from_the_top(size)

    def reset_representor(self):
        self.representor.reset(self.current)

    def show_curr(self):
        self.representor.show_curr()
        pygame.display.flip()

    def end_round(self):
        pass

    def play(self, clock):
        up = None
        while True:
            self.reset_representor()
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if up is None:
                        up = self.representor.collide_with(pygame.mouse.get_pos())
                        if up is not None:
                            self.representor.lift(up)

                    else:
                        compared = self.representor.collide_with(pygame.mouse.get_pos())
                        if compared is None:
                            continue

                        if self.current.are_compatible(up, compared):
                            able_to_erase = self.add_to(compared, self.get_bottle(up).get_top_size(),
                                                        self.get_bottle(up).get_top_color())
                            self.erase_from(up, able_to_erase)
                            print('filled ' + str(self.num_of_filled))
                            if self.get_bottle(compared).is_filled():
                                # trouble is here
                                self.num_of_filled += 1
                                if self.num_of_filled == self.need_to_be_filled:
                                    print('here')
                                    print(self.num_of_filled)
                                    self.end_round()
                                    self.coins += self.plus
                                    return
                            up = None
                            self.show_curr()
                        else:
                            up = None
                            self.show_curr()

                clock.tick(60)

    def game_loop(self):
        clock = pygame.time.Clock()
        self.name, self.num_of_bottles = self.representor.start_screen()
        self.current = BottleSet(self.num_of_bottles)
        self.current.random_filling(2)
        self.initial = self.current
        self.previous = self.current
        self.coins = 0
        self.reset_representor()
        self.show_curr()
        self.play(clock)

