import pygame
import draw.objects


class Renderer:
    def __init__(self):
        pygame.init()
        self.objects = pygame.sprite.LayeredUpdates()
        self.surface = pygame.Surface((960, 960))
        self.screen = pygame.display.set_mode((960, 960))

        # add the robot
        self.objects.add(draw.objects.Robot(), layer=2)

        # add the lidar overlay
        self.objects.add(draw.objects.Lidar(), layer=1)

    def set_grid(self, g):
        # grid should be bottom-most layer
        grid = draw.objects.Grid()
        grid.update_image(g)
        self.objects.add(grid, layer=0)

    def update_robot(self, data):
        robot = self.objects.get_sprites_from_layer(2)[0]
        robot.update(data)

    def paint_lidar(self, data):
        lidar = self.objects.get_sprites_from_layer(1)[0]
        lidar.update(data)

    def update_screen(self):
        self.objects.draw(self.screen)
        pygame.display.flip()
