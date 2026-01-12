import pygame
import math
import random
from car_new import Car
from barriers import Barrier
from brain import NeuralNetwork
import torch


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Car Simulation with AI")
        self.clock = pygame.time.Clock()


        self.brain = NeuralNetwork()
        self.car = Car(15, 25)  # car size is 50x30
        self.epsilon = 1.0  
        self.epsilon_decay = 0.995  
        self.min_epsilon = 0.01  
        self.episode_reward=0

        self.barriers = [
            Barrier(200, 150, 400, 20),
            Barrier(100, 300, 20, 200),
            Barrier(600, 400, 150, 20),
            Barrier(134, 545, 200, 40),
          
            Barrier(400, 500, 300, 20)

        ]
        self.running = True

    def get_AI_action(self, state):
        if random.random() < self.epsilon: 
            return random.randint(0, 2)  
        else:
            with torch.no_grad():
                state_tensor = torch.tensor(state, dtype=torch.float32)
                q_values = self.brain(state_tensor)
                return torch.argmax(q_values).item()  
    

    def handle_collisions(self):
        
        for barrier in self.barriers:
            if self.car.rect.colliderect(barrier.rect):
                return True
        
        
        if (self.car.x < 0 or self.car.x > 800 - self.car.width or
            self.car.y < 0 or self.car.y > 600 - self.car.height):
            return True
        
        return False
    

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

        
            self.screen.fill((0, 0, 0))
            for barrier in self.barriers:
                barrier.draw(self.screen)

        
            self.car.update_sensors(self.screen) 
            
        
            current_state = [d / 300.0 for d in self.car.data]
            action = self.get_AI_action(current_state)

            
            if action == 0:
                self.car.angle += 10
            elif action == 2:
                self.car.angle -= 10
            self.car.speed = 5
            self.car.drive()

            # 5.
            crashed = self.handle_collisions()
            reward = 0
            done = False

            if crashed:
                reward = -50
                done = True
                self.episode_reward = 0
                self.car.x, self.car.y = 400, 300 # Reset
                self.car.angle = 0
            else:
                reward = 1
                self.episode_reward += 1

        
            self.car.update_sensors(self.screen)
            new_state = [d / 300.0 for d in self.car.data]

            
            if len(current_state) == 5 and len(new_state) == 5:
                self.brain.train_step(current_state, action, reward, new_state, done)

            
            if self.epsilon > self.min_epsilon:
                self.epsilon *= self.epsilon_decay

            
            self.car.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    Game().run()
