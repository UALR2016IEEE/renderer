import math
import pygame
import draw.objects
from utils.data_structures import Point3


class Renderer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.update = None

        self.font = pygame.font.SysFont('monospace', 20)
        self.label = self.font.render('Waiting for client connection.', 1, (255, 255, 255))

        self.primary_objects = None
        self.secondary_objects = None
        self.aggregate_lidar = False
        self.cart = False
        self.lidar_lines = True

        self.robot_pos = Point3()

    def reset(self):
        self.screen = pygame.display.set_mode((640, 480))
        self.update = None
        self.aggregate_lidar = False
        self.cart = False
        self.lidar_lines = True
        if self.primary_objects is not None:
            [self.primary_objects.remove_sprites_of_layer(i) for i in range(6)]
        if self.secondary_objects is not None:
            [self.secondary_objects.remove_sprites_of_layer(i) for i in range(3)]

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

    def set_lidar_box(self, data):
        background = self.primary_objects.get_sprites_from_layer(0)[0]
        background.update_box(data)

    def set_grid(self, g):
        # grid should be bottom-most layer
        grid = draw.objects.Grid()
        grid.update_image(g)
        self.primary_objects.add(grid, layer=1)

    def set_points(self, vertex):
        print('primary', len(self.primary_objects.sprites()))
        for name, point in vertex.items():
            p = draw.objects.Point(point)
            self.primary_objects.add(p, layer=4)
            for p2 in point.edges:
                e = draw.objects.Path(point.point, p2.point)
                self.primary_objects.add(e, layer=5)

    def activate_points(self, vertex):
        vertices = self.primary_objects.get_sprites_from_layer(4)
        v_names = [v.name for v in vertex]
        for v in vertices:
            v.update(v_names)

    def update_robot(self, data):
        robot = self.primary_objects.get_sprites_from_layer(3)[0]
        robot.update(data)
        self.robot_pos = data

    def paint_lidar(self, data):
        if self.primary_objects is not None:
            lidar_primary = self.primary_objects.get_sprites_from_layer(2)[0]
            lidar_primary.update(data, cart=self.cart, lines=self.lidar_lines)
        if self.secondary_objects is not None:
            lidar_secondary = self.secondary_objects.get_sprites_from_layer(2)[0]
            lidar_secondary.update(data, cart=self.cart, lines=self.lidar_lines)

        if self.aggregate_lidar and self.secondary_objects is not None:
            lidar_secondary_aggregate = self.secondary_objects.get_sprites_from_layer(1)[0]
            lidar_secondary_aggregate.update(data, aggregate=True, cart=self.cart, lines=self.lidar_lines)

    def update_screen(self):
        if self.update == 'full-simulation':
            self.primary_objects.draw(self.primary)
            self.secondary_objects.draw(self.secondary)
            label = self.font.render('(x= ' + str(self.robot_pos.x) + ', y= ' + str(self.robot_pos.y) + ', r= ' + str(math.degrees(self.robot_pos.r)) + ')', 1, (255, 0, 0))
            self.screen.blit(label, (20, 20))
            mouse = self.font.render('(mx = ' + str(pygame.mouse.get_pos()[0]) + ', my = ' + str(pygame.mouse.get_pos()[1]) + ')', 1, (255, 0, 0))
            self.screen.blit(mouse, (20, 60))
        elif self.update == 'lidar-test':
            self.primary_objects.draw(self.screen)
        else:
            self.screen.blit(self.label, (0, 0))
        pygame.display.flip()
