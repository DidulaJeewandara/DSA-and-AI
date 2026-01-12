import pygame
import math
import random
from assest.autonomous.car_new import Car
from assest.autonomous.barriers import Barrier
from assest.autonomous.brain import NeuralNetwork
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
            
            Barrier(600, 400, 150, 20),
            Barrier(134, 545, 200, 40),
            Barrier(500, 100, 20, 150),
            Barrier(300, 350, 250, 20)

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

        self.goal_x=700
        self.goal_y=500
        self.goal_radius=10

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

        
            self.screen.fill((0, 0, 0))
            for barrier in self.barriers:
                barrier.draw(self.screen)

            pygame.draw.circle(self.screen, (0, 255, 0), (self.goal_x, self.goal_y), 10)

            dist_x = (self.goal_x - self.car.x) / 800.0
            dist_y = (self.goal_y - self.car.y) / 600.0

        
            self.car.update_sensors(self.screen) 
            
        
            current_state = [d / 300.0 for d in self.car.data]+ [dist_x, dist_y]  # added goal distances
            action = self.get_AI_action(current_state)

            
            if action == 0:
                self.car.angle += 10
            elif action == 2:
                self.car.angle -= 10
            self.car.speed = 5
            self.car.drive()

            # 5.
            crashed = self.handle_collisions()
            pixel_dist_to_goal = math.sqrt((self.goal_x - self.car.x)**2 + (self.goal_y - self.car.y)**2)
            reward = 0
            done = False

            if crashed:
                reward = -50
                done = True
                self.episode_reward = 0
                self.car.x, self.car.y = 15,25 # Reset
                
                self.car.angle = 0

            elif pixel_dist_to_goal < 20+self.goal_radius:
                reward = 100
                done = True
                self.episode_reward += 100
                self.car.x, self.car.y = 15, 25 # Reset
                self.car.angle = 0
                self.goal_x = random.randint(50, 750)
                self.goal_y = random.randint(50, 550)
            
            
            else:
                reward = 1
                self.episode_reward += 1

    
            self.car.update_sensors(self.screen)
            new_state = [d / 300.0 for d in self.car.data]+ [dist_x, dist_y]  # added goal distances


            if len(current_state) == 7 and len(new_state) == 7: #added a goal
                self.brain.train_step(current_state, action, reward, new_state, done)

        
            if self.epsilon > self.min_epsilon:
                self.epsilon *= self.epsilon_decay

            
            self.car.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    Game().run()
