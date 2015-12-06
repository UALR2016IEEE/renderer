import pygame
import draw.objects


class Renderer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.update = None

        font = pygame.font.SysFont('monospace', 20)
        self.label = font.render('Waiting for client connection.', 1, (255, 255, 255))

        self.primary_objects = None
        self.secondary_objects = None
        self.aggregate_lidar = False

    def reset(self):
        self.screen = pygame.display.set_mode((640, 480))
        self.update = None
        self.primary_objects = None
        self.secondary_objects = None
        self.aggregate_lidar = False

    def setup_full_simulation(self):
        self.update = 'full-simulation'
        self.screen = pygame.display.set_mode((1920, 960))
        self.primary = self.screen.subsurface((0, 0, 960, 960))
        self.secondary = self.screen.subsurface((960, 0, 960, 960))

        self.primary_objects = pygame.sprite.LayeredUpdates()
        self.secondary_objects = pygame.sprite.LayeredUpdates()

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

    def setup_lidar_test(self):
        self.update = 'lidar-test'
        self.screen = pygame.display.set_mode((960, 960))

        self.primary_objects = pygame.sprite.LayeredUpdates()

        # add the background
        self.primary_objects.add(draw.objects.Background(distances=True), layer=0)
        # add the lidar overlay
        self.primary_objects.add(draw.objects.Lidar(), layer=2)

    def set_grid(self, g):
        # grid should be bottom-most layer
        grid = draw.objects.Grid()
        grid.update_image(g)
        self.primary_objects.add(grid, layer=1)

    def update_robot(self, data):
        robot = self.primary_objects.get_sprites_from_layer(3)[0]
        robot.update(data)

    def paint_lidar(self, data):
        if self.primary_objects is not None:
            lidar_primary = self.primary_objects.get_sprites_from_layer(2)[0]
            lidar_primary.update(data)
        if self.secondary_objects is not None:
            lidar_secondary = self.secondary_objects.get_sprites_from_layer(2)[0]
            lidar_secondary.update(data)

        if self.aggregate_lidar and self.secondary_objects is not None:
            lidar_secondary_aggregate = self.secondary_objects.get_sprites_from_layer(1)[0]
            lidar_secondary_aggregate.update(data, aggregate=True)

    def update_screen(self):
        if self.update == 'full-simulation':
            self.primary_objects.draw(self.primary)
            self.secondary_objects.draw(self.secondary)
        elif self.update == 'lidar-test':
            self.primary_objects.draw(self.screen)
        else:
            self.screen.blit(self.label, (0, 0))
        pygame.display.flip()
