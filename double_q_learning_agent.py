import numpy as np
import random

def flipCoin():
    r = random.random()
    return r < 0.5

class QLearningAgent:
    def __init__(self, state_space_size, action_space_size, learning_rate=0.1, discount_rate=0.95, exploration_rate=1.0, exploration_decay=0.99, min_exploration_rate=0.01):
        self.state_space_size = state_space_size
        self.action_space_size = action_space_size
        self.q_table1 = np.zeros((state_space_size, action_space_size))
        self.q_table2 = np.zeros((state_space_size, action_space_size))
        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.min_exploration_rate = min_exploration_rate

    def choose_action(self, state):
        if np.random.rand() < self.exploration_rate:
            return np.random.randint(self.action_space_size)
        else:
            a_q1 = np.max(self.q_table1[state])
            a_q2 = np.max(self.q_table2[state])
            if a_q1 > a_q2:
                return np.argmax(self.q_table1[state])
            return np.argmax(self.q_table2[state])

    def update_q_table(self, state, action, new_state, reward):
        if flipCoin:
            future_rewards = np.max(self.q_table2[new_state])
            current_q_value = self.q_table1[state, action]
            new_q_value = current_q_value + self.learning_rate * (reward + self.discount_rate * future_rewards - current_q_value)
            self.q_table1[state, action] = new_q_value
        else:
            future_rewards = np.max(self.q_table1[new_state])
            current_q_value = self.q_table2[state, action]
            new_q_value = current_q_value + self.learning_rate * (reward + self.discount_rate * future_rewards - current_q_value)
            self.q_table2[state, action] = new_q_value

        self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)
