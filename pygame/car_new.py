import pygame
import math

class Car:
    def __init__(self, x, y, angle=0):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 0
        self.max_speed = 10
        self.acceleration = 0.2
        self.deceleration = 0.1
        self.turn_speed = 5
        
        self.width = 50
        self.height = 30
        self.color = (0, 255, 255) # Cyan
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface.fill(self.color)
        self.rect = self.surface.get_rect(center=(self.x, self.y))

        # SENSORS
        self.radars = [] # For drawing lines
        self.data = []   # For the AI (Distances)

    def drive(self):
        # 1. Physics (Move the car)
        rad_angle = math.radians(self.angle)
        self.x += self.speed * math.cos(rad_angle)
        self.y += self.speed * math.sin(rad_angle)
        self.rect.center = (self.x, self.y)
        
        # NOTE: We do NOT clear sensors here anymore. 
        # We handle sensors in 'update_sensors'

    def update_sensors(self, game_map):
        """Scans all 5 angles and populates self.data with 5 distances"""
        self.radars.clear()
        self.data.clear()
        
        # We MUST scan these exact 5 angles to match the Brain's input size (5)
        for degree in [-90, -45, 0, 45, 90]:
            self._cast_ray(degree, game_map)

    def _cast_ray(self, degree, game_map):
        """Internal helper to cast a single ray"""
        length = 0
        x = int(self.rect.center[0])
        y = int(self.rect.center[1])
        
        # Calculate angle of this specific ray relative to car's angle
        ray_angle = math.radians(self.angle + degree)

        # Raycast Loop
        while length < 300:
            length += 1
            # Get tip of the ray
            x = int(self.rect.center[0] + math.cos(ray_angle) * length)
            y = int(self.rect.center[1] + math.sin(ray_angle) * length)

            # Check screen bounds
            if 0 <= x < 800 and 0 <= y < 600:
                # Check color (If not black, it's a wall)
                if game_map.get_at((x, y)) != (0, 0, 0, 255):
                    break
            else:
                break

        # Save Data
        dist = int(math.sqrt(math.pow(x - self.rect.center[0], 2) + math.pow(y - self.rect.center[1], 2)))
        self.radars.append([(x, y), dist])
        self.data.append(dist)

    def draw(self, screen):
        # Draw Sensors
        for r in self.radars:
            pos = r[0]
            pygame.draw.line(screen, (0, 255, 0), self.rect.center, pos, 1)
            pygame.draw.circle(screen, (0, 255, 0), pos, 5)

        # Draw Car
        rotated_surface = pygame.transform.rotate(self.surface, -self.angle)
        rect = rotated_surface.get_rect(center=(self.x, self.y))
        screen.blit(rotated_surface, rect.topleft)