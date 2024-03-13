from double_q_learning_agent import DoubleQLearningAgent
import numpy as np
from game import Game
import time
from plot import plot_performance

max_lives = 3

def encode_state(player_lives, dealer_lives, live_bullets, blank_bullets):
    return (player_lives +
            dealer_lives +
            live_bullets +
            blank_bullets)

def train_agent(episodes=200, test_episodes=1):
    game = Game()
    total_bullets = game.getTotalBullets()
    state_space_size = ((max_lives) + (max_lives) + (total_bullets) + (total_bullets))
    action_space_size = 2
    agent = DoubleQLearningAgent(state_space_size, action_space_size)
    total_rewards = []
    win_counts = {"learning_phase_wins": 0, "testing_phase_wins": 0}
    exploration_rates = []
    wins_per_episode = []
    
    learning_player_wins = 0
    testing_player_wins = 0
    random_agent_wins = 0

    for episode in range(episodes):
        total_reward = 0
        game.reset()
        initial_state = game.get_initial_state()
        state_encoded = encode_state(*initial_state)
        
        # Disable exploration for the testing phase
        if episode >= episodes - test_episodes:
            agent.exploration_rate = 0
        
        while not game.is_over():
            if episode >= episodes - test_episodes:
                print("*" * 20)
            action = agent.choose_action(state_encoded)
            if episode >= episodes - test_episodes:
                print(f"Episode {episode + 1}:")
                print(f"Live Bullets: {game.bullets.count(1)} and Blank Bullets: {game.bullets.count(0)}")
                print(f"Current State: Bullet Index {game.current_bullet_index}, Player Lives {game.player_lives}, Dealer Lives {game.dealer_lives}, Rounds {game.rounds}")
                print(f"Agent Action: {'Shoot Dealer' if action == 1 else 'Shoot Self'}")
                print(f"Bullet was {'live' if game.bullets[game.current_bullet_index] else 'blank'}")
                print("-" * 20)
                time.sleep(2)
            reward, game_over, next_state = game.play_step(action)
            next_state_encoded = encode_state(*next_state)
            total_reward+=reward
            total_rewards.append(total_reward)
            exploration_rates.append(agent.exploration_rate)
            if episode >= episodes - test_episodes:
                print(f"Dealer Action: {'Shoot Agent' if game.getDealerDecision() == 1 else 'Shoot Self'}")
                print(f"Bullet was {'live' if game.bullets[game.current_bullet_index] else 'blank'}")
                print(f"Player lives now {game.player_lives} and dealer lives now {game.dealer_lives}")
                print(f"Reward: {reward}")
                print("-" * 20)
                time.sleep(2) 

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

        game.reset()
        while not game.is_over():
            action = np.random.choice(action_space_size)
            _, game_over, _ = game.play_step(action)
            
            if game_over:
                break

        if game.player_lives > game.dealer_lives:
            if episode >= episodes - test_episodes:
                win_counts["testing_phase_wins"] += 1
            else:
                win_counts["learning_phase_wins"] += 1

        wins_per_episode.append(win_counts["learning_phase_wins"] + win_counts["testing_phase_wins"])

        
        if game.player_lives > game.dealer_lives:
            random_agent_wins += 1

    print(f"Learning Phase Wins (Double Q-learning): {learning_player_wins} ({(learning_player_wins/(episodes - test_episodes))*100:.2f}%)")
    print(f"Testing Phase Wins (Double Q-learning): {testing_player_wins} ({(testing_player_wins/test_episodes)*100:.2f}%)")
    print(f"Random Agent Wins: {random_agent_wins} ({(random_agent_wins/episodes)*100:.2f}%)")

    np.savetxt("data1.txt", agent.q_table1, fmt='%f')
    np.savetxt("data2.txt", agent.q_table2, fmt='%f')

    return total_rewards, exploration_rates, wins_per_episode


if __name__ == "__main__":
    total_rewards, exploration_rates, wins_per_episode = train_agent()
    plot_performance(total_rewards, exploration_rates, wins_per_episode)

