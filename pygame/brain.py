import torch
import torch.nn as nn
import torch.nn.functional as F
import random

class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.number_of_actions = 3  # e.g., turn left, go straight, turn right
        self.gamma=0.9

        self.model = nn.Sequential(
            nn.Linear(5, 128),  # Assuming 5 input features
            nn.ReLU(),#activation function
            nn.Linear(128,self.number_of_actions)
        )

        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)#optimizer
        self.loss_function = nn.MSELoss()  # MeanSquared Error loss

    def forward(self, state):
            state = torch.tensor(state, dtype=torch.float32)
            return self.model(state)
        
    def train_step(self, state, action, reward, next_state, done):
            state = torch.tensor(state, dtype=torch.float32)
            next_state = torch.tensor(next_state, dtype=torch.float32)
            action = torch.tensor(action, dtype=torch.int64)
            reward = torch.tensor(reward, dtype=torch.float32)

            # Predict Q values for current state
            pred = self.model(state)

            # FIXED: Initialize target as a copy of predictions (not reward)
            target = pred.clone()

            # Calculate new Q-value
            q_new = reward
            if not done:
                q_new = reward + self.gamma * torch.max(self.model(next_state))
            
            # Update the Q-value for the action taken
            target[action] = q_new
            
            # Backpropagation
            self.optimizer.zero_grad()
            loss = self.loss_function(target, pred)
            loss.backward()
            self.optimizer.step()