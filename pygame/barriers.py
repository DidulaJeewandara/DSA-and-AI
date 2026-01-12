import pygame

class Barrier:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width 
        self.height = height
        self.color = (200, 0, 0)  # Red color for barriers
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))