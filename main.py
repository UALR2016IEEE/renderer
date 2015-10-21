import pygame
import numpy as np
import status_io.server
import draw.renderer


def main():

    r = draw.renderer.Renderer()
    s = status_io.server.IOHandler()
    s.start()
    clock = pygame.time.Clock()

    running = True

    while not s.halt.value:
        # process server data
        if not s.incoming.empty():
            data = s.incoming.get()
            if data[0] == 'grid-colors':
                # stupid x/y axis differences
                r.set_grid(data[1])
            if data[0] == 'robot-pos':
                r.update_robot(data[1])
            if data[0] == 'lidar-points':
                r.paint_lidar(data[1])

        # process pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                s.finish()
                pygame.quit()
                running = False

        if running:
            # update the screen
            r.update_screen()
            clock.tick(60)

if __name__ == '__main__':
    np.set_printoptions(threshold=99999999, linewidth=9999999)
    main()
