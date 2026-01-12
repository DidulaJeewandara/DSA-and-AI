import pygame
from pygame.math import Vector2
from assest.normal_game.car import Car 
from assest.normal_game.old_barrier import Barrier
import math


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
    
        
        
        
        pygame.display.set_caption("Car Simulation")
        self.clock = pygame.time.Clock()
        self.car = Car(15,25)  #car size is 

        self.barriers = [
            Barrier(200, 150, 400, 20),
            Barrier(100, 300, 20, 200),
            Barrier(600, 400, 150, 20),
            Barrier(134, 545, 200, 40),
            Barrier(500, 100, 20, 150),
            Barrier(300, 350, 250, 20),
            Barrier(700, 250, 20, 200),
            Barrier(400, 500, 300, 20)
            
        ]
        self.running = True

    def handling_input(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                if self.car.speed < self.car.max_speed  : 
                         self.car.speed += self.car.acceleration
            elif keys[pygame.K_DOWN]:
                if self.car.speed > -self.car.max_speed:
                    self.car.speed += -self.car.acceleration
            else:
                if self.car.speed > 0:
                    self.car.speed -= self.car.deceleration
                elif self.car.speed < 0:
                    self.car.speed += self.car.deceleration

            if keys[pygame.K_LEFT]:
                self.car.angle -= self.car.turn_speed
            if keys[pygame.K_RIGHT]:
                self.car.angle += self.car.turn_speed
            
            if self.car.x<0:
                self.car.x=0
                self.car.speed=0
            if self.car.x>800-self.car.width:
                self.car.x=800-self.car.width
                self.car.speed=0

            if self.car.y<0:
                self.car.y=0
                self.car.speed=0
            if self.car.y>600-self.car.height:
                self.car.y=600-self.car.height
                self.car.speed=0        
            
    def handle_collisions(self):
           for barrier in self.barriers:
               if self.car.rect.colliderect(barrier.rect):
                       self.car.speed = -self.car.speed * self.car.bounce

                       rad_angle = math.radians(self.car.angle)
                       self.car.x += self.car.speed * math.cos(rad_angle)
                       self.car.y += self.car.speed * math.sin(rad_angle)
                       self.car.rect.center = (self.car.x, self.car.y)
                           
            
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

          

            self.handling_input()
            self.handle_collisions()

            self.car.drive()

            
            self.screen.fill((0, 0, 0))
            self.car.draw(self.screen)
            for barrier in self.barriers:
                barrier.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    Game().run()