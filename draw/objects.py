import pygame
import math


class Grid(pygame.sprite.Sprite):
    # g is the numpy color array
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([960, 960])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()

    def update_image(self, g):
        self.image = pygame.surfarray.make_surface(g)

    def update(self):
        pass


class Robot(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # generate 'robot' sprite
        self.imageMaster = pygame.Surface([60, 60])
        pygame.draw.rect(self.imageMaster, (0, 0, 255), (0, 0, 60, 60))
        pygame.draw.rect(self.imageMaster, (0, 0, 0, 255), (10, 10, 40, 40))
        pygame.draw.circle(self.imageMaster, (255, 255, 255), (30, 30), 10)
        pygame.draw.line(self.imageMaster, (255, 0, 0), (30, 30), (60, 30))
        self.imageMaster = self.imageMaster.convert_alpha()
        
        self.image = self.imageMaster
        self.rect = self.image.get_rect()
        self.rect.center = (30, 30)

    def update(self, data):
        center = data.x, data.y
        self.rect.center = center
        self.image = pygame.transform.rotate(self.imageMaster, math.degrees(data.r))
        self.rect = self.image.get_rect()
        self.rect.center = center


class Lidar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([960, 960])
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()

    def update(self, data, aggregate=False):
        if not aggregate:
            # print(data[0].x, data[0].y, math.degrees(data[0].r))
            self.image.fill((0, 0, 0))
        rx = data[0].x
        ry = data[0].y
        angle = data[0].r
        scans = data[1]

        first = True

        for idx in range(scans.shape[1]):
            if scans[0, idx] > 0:
                # turn scan data back to tenths of an inch
                dx = scans[0, idx] * math.cos(scans[1, idx] + angle) / 2.54
                dy = -scans[0, idx] * math.sin(scans[1, idx] + angle) / 2.54
                # print('dx', dx, 'dy', dy, 'angle', math.degrees(scan[1] + angle), 'x-adjust', (math.cos(scan[1] + angle)), 'y-adjust', (math.sin(scan[1] + angle)))

                fx = int(rx + dx)
                fy = int(ry + dy)

                pygame.draw.rect(self.image, (255, 0, 0), (int(rx + dx), int(ry + dy), 2, 2))
                if not aggregate:
                    if first:
                        pygame.draw.line(self.image, (0, 0, 255), (rx, ry), (int(fx), int(fy)))
                        pygame.draw.rect(self.image, (0, 0, 255), (int(fx), int(fy), 2, 2))
                        first = False
                    else:
                        pygame.draw.line(self.image, (255, 0, 0), (rx, ry), (int(fx), int(fy)))


class Background(pygame.sprite.Sprite):
    def __init__(self, distances=False):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([960, 960])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()

        if distances:
            self.make_distance_circles()

    def make_distance_circles(self):
        for i in range(1, 5):
            pygame.draw.circle(self.image, (128, 128, 128), (480, 480), i * 120, 4)
