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
        center = (data[0], data[1])
        self.rect.center = center
        self.image = pygame.transform.rotate(self.imageMaster, math.degrees(data[2]))
        self.rect = self.image.get_rect()
        self.rect.center = center
