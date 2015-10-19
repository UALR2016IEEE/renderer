import pygame


class Renderer:
    def __init__(self):
        pygame.init()
        self.surface = pygame.Surface((960, 960))
        self.screen = pygame.display.set_mode((960, 960))

    @property
    def grid(self):
        return self._grid

    @grid.setter
    def grid(self, g):
        self._grid = g
        self.update_surface()

    def update_surface(self):
        self.surface = pygame.surfarray.make_surface(self.grid)

    def update_screen(self):
        self.screen.blit(self.surface, (0, 0))
        pygame.display.flip()
