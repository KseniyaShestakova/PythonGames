from presentation import *

X_WIDTH = 400
Y_WIDTH = 400

pygame.init()

screen = pygame.display.set_mode((X_WIDTH, Y_WIDTH))
screen.fill((204, 204, 255))

color_list = [(0, 0, 205), (255, 140, 0), (135, 206, 235), (0, 255, 255), (250, 128, 114),
              (154, 205, 50), (139, 0, 139), (255, 215, 0)]

bottle_set = BottleSet(10, 4)
bottle_set.random_filling()

background_color = (204, 204, 255)
border_color = (96, 96, 96)
border_width = 2

representor = Representor(X_WIDTH, Y_WIDTH, bottle_set)

# representor.draw_bottle_set(screen, color_list, bottle_set)
representor.start_screen(screen)

screen.blit(screen, (0, 0))


pygame.display.flip()
time.sleep(60)

pygame.quit()
