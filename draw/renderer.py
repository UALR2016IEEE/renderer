import pygame
import draw.objects


class Renderer:
    def __init__(self):
        pygame.init()
        self.primary_objects = pygame.sprite.LayeredUpdates()
        self.secondary_objects = pygame.sprite.LayeredUpdates()

        self.surface = pygame.Surface((1920, 960))

        self.screen = pygame.display.set_mode((1920, 960))
        self.primary = self.screen.subsurface((0, 0, 960, 960))
        self.secondary = self.screen.subsurface((960, 0, 960, 960))

        # add the backgrounds
        self.primary_objects.add(draw.objects.Background(), layer=0)
        self.secondary_objects.add(draw.objects.Background(), layer=0)

        # add the robot
        self.primary_objects.add(draw.objects.Robot(), layer=3)

        # add the lidar overlay
        self.primary_objects.add(draw.objects.Lidar(), layer=2)
        self.secondary_objects.add(draw.objects.Lidar(), layer=2)

        # add the lidar aggregate overlay
        self.secondary_objects.add(draw.objects.Lidar(), layer=1)
        self.aggregate_lidar = True

    def set_grid(self, g):
        # grid should be bottom-most layer
        grid = draw.objects.Grid()
        grid.update_image(g)
        self.primary_objects.add(grid, layer=1)

    def update_robot(self, data):
        robot = self.primary_objects.get_sprites_from_layer(3)[0]
        robot.update(data)

    def paint_lidar(self, data):
        lidar_primary = self.primary_objects.get_sprites_from_layer(2)[0]
        lidar_secondary = self.secondary_objects.get_sprites_from_layer(2)[0]

        lidar_primary.update(data)
        lidar_secondary.update(data)

        if self.aggregate_lidar:
            lidar_secondary_aggregate = self.secondary_objects.get_sprites_from_layer(1)[0]
            lidar_secondary_aggregate.update(data, aggregate=True)

    def update_screen(self):
        self.primary_objects.draw(self.primary)
        self.secondary_objects.draw(self.secondary)
        pygame.display.flip()
