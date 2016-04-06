import pygame
import numpy as np
import status_io.server
import draw.renderer
import simulate.controller
from utils.data_structures import Point3
import math


def main():

    lidar_pos = Point3(480, 480, math.radians(90))
    r = draw.renderer.Renderer()
    s = status_io.server.IOHandler()
    s.start()
    clock = pygame.time.Clock()

    running = True

    while not s.halt.value:
        # process server data
        if not s.incoming.empty():
            data = s.incoming.get()

            # top level render control commands
            if data[0] == 'reset':
                r.reset()
            elif data[0] == 'full-simulation':
                r.reset()
                r.setup_full_simulation()

                # have the server set up the grid by defualt - can still do grid-colors and reset if needed
                sim = simulate.controller.Controller(Point3())
                sim.init_grid()
                r.set_grid(sim.grid.get_pygame_grid())
            elif data[0] == 'lidar-test':
                r.reset()
                r.setup_lidar_test()
            elif data[0] == 'lidar-cart':
                r.cart = True

            # commands used for full-simulation rendering
            elif data[0] == 'grid-colors':
                # stupid x/y axis differences
                r.set_grid(data[1])
            elif data[0] == 'robot-pos':
                r.update_robot(data[1])
            elif data[0] == 'lidar-points':
                r.paint_lidar(data[1])
            elif data[0] == 'add-points':
                r.set_points(data[1])
            elif data[0] == 'activate-points':
                r.activate_points(data[1])

            # commands used for lidar-test rendering
            elif data[0] == 'lidar-test-points':
                r.paint_lidar((lidar_pos, data[1]))

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
