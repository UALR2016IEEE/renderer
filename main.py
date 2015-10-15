import pygame
import numpy as np
import grid as grid
import sys
import status_io.server


def main():

    pygame.init()
    surface = pygame.Surface((96, 96))

    g = grid.Grid()

    surface = pygame.surfarray.make_surface(g.get_pygame_grid())
    surface = pygame.transform.scale(surface, (1024, 1024))
    screen = pygame.display.set_mode((1024, 1024))
    screen.blit(surface, (0, 0))
    pygame.display.flip()

    s = status_io.server.IOHandler()
    s.start()

    pause = False

    while not pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    np.set_printoptions(threshold=99999999, linewidth=9999999)
    main()
