import pygame
from pygame.math import Vector2
from car import Car 


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Car Simulation")
        self.clock = pygame.time.Clock()
        self.car = Car(400, 300)
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                if self.car.speed < self.car.max_speed:
                    self.car.speed += self.car.acceleration
            elif keys[pygame.K_DOWN]:
                if self.car.speed > -self.car.max_speed / 2:
                    self.car.speed -= self.car.deceleration
            else:
                if self.car.speed > 0:
                    self.car.speed -= self.car.deceleration
                elif self.car.speed < 0:
                    self.car.speed += self.car.deceleration

            if keys[pygame.K_LEFT]:
                self.car.angle += self.car.turn_speed
            if keys[pygame.K_RIGHT]:
                self.car.angle -= self.car.turn_speed

            self.car.drive()

            self.screen.fill((0, 0, 0))
            self.car.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    Game().run()