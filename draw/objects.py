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


class Point(pygame.sprite.Sprite):
    def __init__(self, vertex):
        pygame.sprite.Sprite.__init__(self)

        self.vertex = vertex

        # make a sprite for the point
        self.imageMasterNormal = pygame.Surface([10, 10])
        pygame.draw.rect(self.imageMasterNormal, (0, 0, 255), (0, 0, 10, 10))
        self.imageMasterNormal = self.imageMasterNormal.convert_alpha()

        self.imageMasterStart = pygame.Surface([10, 10])
        pygame.draw.rect(self.imageMasterStart, (255, 0, 255), (0, 0, 10, 10))
        self.imageMasterStart = self.imageMasterStart.convert_alpha()

        self.imageMasterOnPath = pygame.Surface([10, 10])
        pygame.draw.rect(self.imageMasterOnPath, (128, 128, 128), (0, 0, 10, 10))
        self.imageMasterOnPath = self.imageMasterOnPath.convert_alpha()

        self.imageMasterEnd = pygame.Surface([10, 10])
        pygame.draw.rect(self.imageMasterEnd, (0, 255, 255), (0, 0, 10, 10))
        self.imageMasterEnd = self.imageMasterEnd.convert_alpha()

        self.image = self.imageMasterNormal
        self.rect = self.image.get_rect()
        self.rect.center = (self.vertex.point.x, self.vertex.point.y)

    def update(self, names):
        # if in list, activate
        try:
            if names.index(self.vertex.name) == 0:
                self.image = self.imageMasterStart
            elif names.index(self.vertex.name) == len(names) - 1:
                self.image = self.imageMasterEnd
            elif names.index(self.vertex.name) > -1:
                self.image = self.imageMasterOnPath
            else:
                self.image = self.imageMasterNormal
        except ValueError:
            pass


class Path(pygame.sprite.Sprite):
    def __init__(self, p1, p2):
        pygame.sprite.Sprite.__init__(self)

        # make a sprite for the point
        self.imageMasterNormal = pygame.Surface([960, 960])
        self.imageMasterNormal.fill((0, 0, 0))
        self.imageMasterNormal.set_colorkey((0, 0, 0))
        pygame.draw.line(self.imageMasterNormal, (0, 0, 255), (p1.x, p1.y), (p2.x, p2.y))
        self.imageMasterNormal = self.imageMasterNormal.convert_alpha()

        self.imageMasterActive = pygame.Surface([960, 960])
        self.imageMasterActive.fill((0, 0, 0))
        self.imageMasterActive.set_colorkey((0, 0, 0))
        pygame.draw.line(self.imageMasterActive, (0, 0, 255), (p1.x, p1.y), (p2.x, p2.y))
        self.imageMasterActive = self.imageMasterActive.convert_alpha()

        self.image = self.imageMasterNormal
        self.rect = self.image.get_rect()
        self.rect.center = (480, 480)

    def update(self, active):
        if active:
            self.image = self.imageMasterActive
        else:
            self.image = self.imageMasterNormal


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

    def update(self, data, aggregate=False, cart=False, lines=False):
        if not aggregate:
            # print(data[0].x, data[0].y, math.degrees(data[0].r))
            self.image.fill((0, 0, 0))
        rx = data[0].x
        ry = data[0].y
        angle = data[0].r
        scans = data[1]

        first = True

        for idx in range(scans.shape[1]):
            # turn scan data back to tenths of an inch
            if cart:
                # get magnitude rho
                rho = math.sqrt(scans[0, idx] ** 2 + scans[1, idx] ** 2)
                phi = math.atan2(scans[1, idx], scans[0, idx])
                dx = rho * math.cos(phi) / 2.54
                dy = -rho * math.sin(phi) / 2.54
            else:
                dx = scans[0, idx] * math.cos(scans[1, idx]) / 2.54
                dy = -scans[0, idx] * math.sin(scans[1, idx]) / 2.54
            # print('dx', dx, 'dy', dy, 'angle', math.degrees(scan[1] + angle), 'x-adjust', (math.cos(scan[1] + angle)), 'y-adjust', (math.sin(scan[1] + angle)))

            fx = int(rx + dx)
            fy = int(ry + dy)

            if cart or scans[0, idx] > 0:
                # plot the terminating point of the scan as a red dot
                pygame.draw.rect(self.image, (255, 0, 0), (int(rx + dx), int(ry + dy), 2, 2))
                if not aggregate:
                    if first:
                        # first line gets to be blue
                        if lines:
                            pygame.draw.line(self.image, (0, 0, 255), (rx, ry), (int(fx), int(fy)))
                        pygame.draw.rect(self.image, (0, 0, 255), (int(fx), int(fy), 2, 2))
                        first = False
                    elif lines:
                        # rest of the lines are red
                        pygame.draw.line(self.image, (255, 0, 0), (rx, ry), (int(fx), int(fy)))


class Background(pygame.sprite.Sprite):
    def __init__(self, distances=False):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([960, 960])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.distances = distances

        if self.distances:
            self.make_distance_circles()

    def make_distance_circles(self):
        for i in range(1, 5):
            pygame.draw.circle(self.image, (128, 128, 128), (480, 480), i * 120, 4)
        # pygame.draw.rect(self.image, (0, 0, 255), (480 - (200 / 2.54), 480 - (180 / 2.54), 400 / 2.54, 220 / 2.54), 1)
            
    def update_box(self, data):
        # need to regenerate background
        self.image = pygame.Surface([960, 960])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()

        if self.distances:
            self.make_distance_circles()

        # box region is defined as ((x_lower, x_upper), (y_lower, y_upper))
        x = data[0][0] / 2.54
        w = (data[0][1] - data[0][0]) / 2.54
        y = data[1][0] / 2.54
        h = (data[1][1] - data[1][0]) / 2.54
        pygame.draw.rect(self.image, (0, 0, 255), (480 - x, 480 - y, w, h), 1)
