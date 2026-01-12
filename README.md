# Autonomous Car using Deep Q-Learning (DQN)

A self-driving car simulation built from scratch in Python, trained using Reinforcement Learning.

Tech Stack:

Simulation: Custom PyGame environment (Physics & Raycasting Sensors).

AI: PyTorch (Deep Q-Network with Experience Replay).


How should you ready your pc or laptop to run this small game:

      you will be needed to install pytorch,pygame and numpy libraries
      
how to start:
there will be two folders,
one is autonomous and other_one is normal_game .Inside the normal game folder you will find a main.py and if u run it ,u will find a simple car game.

Inside the autonomous folder u will find a new_main.py.If u run it you will find an DQN autonomus car.
How it works: The car casts 7 ray-traced "sensors" to measure distance to walls and to messure the distance to a specific goal. These inputs are fed into a Neural Network which outputs steering commands (Left, Straight, Right). The agent learns via a reward system (+1 for survival, minus reward for a crash.


