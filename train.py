from q_learning_agent import QLearningAgent
import numpy as np
from game import Game
import time
import matplotlib.pyplot as plt

max_lives = 3

def calculate_base(offsets):
    base = [1]
    for offset in offsets[:-1]:
        base.append(base[-1] * offset)
    return base[::-1]

def encode_state(player_lives, dealer_lives, live_bullets, blank_bullets):
    total_bullets_remaining = live_bullets + blank_bullets
    probability_live_next = int((live_bullets / total_bullets_remaining if total_bullets_remaining > 0 else 0)*100)
    probability_blank_next = int((blank_bullets / total_bullets_remaining if total_bullets_remaining > 0 else 0)*100)

    offsets = [max_lives + 1, max_lives + 1, 101, 101]
    base = calculate_base(offsets)

    state_index = (player_lives + dealer_lives + probability_live_next + probability_blank_next) * base

    return state_index

def train_agent(episodes=1000, test_episodes=0):

    game = Game()
    total_bullets = game.getTotalBullets()
    state_space_size = ((max_lives) * (max_lives) * (100) * (100))
    action_space_size = 2
    total_reward=0
    agent = QLearningAgent(state_space_size, action_space_size)
    
    learning_player_wins = 0
    testing_player_wins = 0
    random_agent_wins = 0
    
    shoot_dealer_count = 0
    shoot_self_count = 0

    total_rewards = [] 
    action_counts = {'shoot_dealer': [], 'shoot_self': []}

    for episode in range(episodes):
        game.reset()
        initial_state = game.get_initial_state()
        state_encoded = encode_state(*initial_state)
        
        # Disable exploration for the testing phase
        if episode >= episodes - test_episodes:
            agent.exploration_rate = 0
        
        while not game.is_over():
            action = agent.choose_action(state_encoded)
            
            # Increment counters based on the action chosen by the agent
            if action == 0:
                shoot_self_count += 1
            else:
                shoot_dealer_count += 1
            
            reward, game_over, next_state = game.play_step(action)
            next_state_encoded = encode_state(*next_state)
            total_reward += reward
            
            if episode < episodes - test_episodes:
                agent.update_q_table(state_encoded, action, next_state_encoded, reward)
            
            if game_over:
                break
            
            state_encoded = next_state_encoded

        if game.player_lives > game.dealer_lives:
            if episode >= episodes - test_episodes:
                testing_player_wins += 1
            else:
                learning_player_wins += 1

        total_rewards.append(total_reward)
        action_counts['shoot_dealer'].append(shoot_dealer_count)
        action_counts['shoot_self'].append(shoot_self_count)
        game.reset()
        while not game.is_over():
            action = np.random.choice(action_space_size)
            _, game_over, _ = game.play_step(action)
            
            if game_over:
                break
        
        if game.player_lives > game.dealer_lives:
            random_agent_wins += 1

    print(f"Learning Phase Wins (Q-learning): {learning_player_wins} ({(learning_player_wins/(episodes - test_episodes))*100:.2f}%)")
    if test_episodes > 0:
        print(f"Testing Phase Wins (Q-learning): {testing_player_wins} ({(testing_player_wins/test_episodes)*100:.2f}%)")
    print(f"Random Agent Wins: {random_agent_wins} ({(random_agent_wins/episodes)*100:.2f}%)")
    print(f"Agent chose 'Shoot Dealer' {shoot_dealer_count} times.")
    print(f"Agent chose 'Shoot Self' {shoot_self_count} times.")

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(total_rewards)
    plt.title('Total Rewards per Episode')
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')

    plt.subplot(1, 2, 2)
    plt.plot(action_counts['shoot_dealer'], label='Shoot Dealer')
    plt.plot(action_counts['shoot_self'], label='Shoot Self')
    plt.title('Action Selection Over Episodes')
    plt.xlabel('Episode')
    plt.ylabel('Count')
    plt.legend()

    plt.tight_layout()
    plt.show()

    np.savetxt("data.txt", agent.q_table, fmt='%f')

if __name__ == "__main__":
    train_agent()
