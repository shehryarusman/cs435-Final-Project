import numpy as np

class QLearningAgent:
    def __init__(self, state_space_size, action_space_size, learning_rate=0.1, discount_rate=0.95, exploration_rate=1.0, exploration_decay=0.99, min_exploration_rate=0.01):
        self.state_space_size = state_space_size
        self.action_space_size = action_space_size
        self.q_table = np.zeros((state_space_size, action_space_size))
        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.min_exploration_rate = min_exploration_rate

    def choose_action(self, state):
        if np.random.rand() < self.exploration_rate:
            return np.random.randint(self.action_space_size)
        else:
            return np.argmax(self.q_table[state])

    def update_q_table(self, state, action, new_state, reward):
        future_rewards = np.max(self.q_table[new_state])
        current_q_value = self.q_table[state, action]
        new_q_value = current_q_value + self.learning_rate * (reward + self.discount_rate * future_rewards - current_q_value)
        self.q_table[state, action] = new_q_value

        self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)
