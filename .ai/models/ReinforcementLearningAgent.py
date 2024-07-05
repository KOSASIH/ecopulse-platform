import gym
import numpy as np
from stable_baselines3 import PPO

class ReinforcementLearningAgent:
    def __init__(self, env_name, model_path):
        self.env = gym.make(env_name)
        self.model = PPO.load(model_path)

    def train(self, num_episodes):
        for episode in range(num_episodes):
            obs = self.env.reset()
            done = False
            rewards = 0
            while not done:
                action, _ = self.model.predict(obs)
                obs, reward, done, _ = self.env.step(action)
                rewards += reward
            print(f"Episode {episode+1}, Reward: {rewards}")

    def test(self, num_episodes):
        for episode in range(num_episodes):
            obs = self.env.reset()
            done = False
            rewards = 0
            while not done:
                action, _ = self.model.predict(obs)
                obs, reward, done, _ = self.env.step(action)
                rewards += reward
            print(f"Episode {episode+1}, Reward: {rewards}")
