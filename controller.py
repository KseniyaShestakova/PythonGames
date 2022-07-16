from presentation import *


class Controller:
    name = ''
    coins = 0
    initial = BottleSet()
    current = BottleSet()
    previous = BottleSet()
    num_of_bottles = initial.num_of_bottles
    num_empty = 2
    representor = None

    def __init__(self, _bottle_set=BottleSet(), _width=600, _height=600,
                 _color_spectrum=((0, 0, 205), (255, 140, 0), (135, 206, 235),
                                  (0, 255, 255), (250, 128, 114),
                                  (154, 205, 50), (139, 0, 139), (255, 215, 0)),
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

    def restart(self):
        self.current = self.initial
        self.previous = self.initial

    def step_back(self):
        # can be applied once
        self.current = self.previous

    def get_bottle(self, num):
        # may be returns copy
        return self.current.bottle_list[num]

    def add_to(self, num, size=1):
        return self.current.bottle_list[num].add_to_the_top(size)

    def erase_from(self, num, size=1):
        self.current.bottle_list[num].erase_from_the_top(size)

    def reset_representor(self):
        self.representor.reset(self.current)

    def game_loop(self):
        clock = pygame.time.Clock()
        self.name = self.representor.start_screen()
        print("go on")
        self.coins = 0
        up = None
        while True:
            self.reset_representor()
            self.representor.show_curr()
            for event in pygame.event.get():
                self.representor.show_curr()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if up is None:
                        up = self.representor.collide_with(pygame.mouse.get_pos())
                        print(up)
                        if up is not None:
                            print("lift")
                            self.representor.lift(up)
                            pygame.display.flip()
                    else:
                        compared = self.representor.collide_with(pygame.mouse.get_pos())
                        if compared is None:
                            continue
                        print(compared)
                        if self.current.are_compatible(up, compared):
                            # trouble is here
                            able_to_erase = self.add_to(compared, self.get_bottle(up).get_size_of_empty_space())
                            self.erase_from(up, able_to_erase)
                            up = None

                clock.tick(60)



