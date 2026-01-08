import pygame
import math

class Car:
    def __init__(self, x, y, angle=0):
        self.x = x #x is position on x axis
        self.y = y   #y is position on y axis
        self.angle = angle  # in degrees
        self.speed = 0
        self.max_speed = 10
        self.acceleration = 0.2
        self.deceleration = 0.1
        self.turn_speed = 5  # degrees per frame
        self.width = 50
        self.height = 30
        self.color = (250, 225, 234)  # RGB color
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface.fill(self.color)

    def drive(self):
        # Update position based on speed and angle
        rad_angle = math.radians(self.angle)
        self.x += self.speed * math.cos(rad_angle)
        self.y += self.speed * math.sin(rad_angle)
    
    def draw(self, screen):
        # Rotate the car surface and draw it on the screen
        rotated_surface = pygame.transform.rotate(self.surface, -self.angle)
        rect = rotated_surface.get_rect(center=(self.x, self.y))
        screen.blit(rotated_surface, rect.topleft)
