import pygame
import numpy as np
import sys
import status_io.server
import draw.renderer


def main():

    r = draw.renderer.Renderer()
    s = status_io.server.IOHandler()
    s.start()

    while not s.halt:
        # process server data
        while not s.incoming.empty():
            data = s.incoming.get()
            if data[0] == 'grid-colors':
                # stupid x/y axis differences
                r.set_grid(data[1])
            if data[0] == 'robot-pos':
                r.update_robot(data[1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pause = True
                s.stop()
                pygame.quit()
                sys.exit()
        r.update_screen()


if __name__ == '__main__':
    np.set_printoptions(threshold=99999999, linewidth=9999999)
    main()
