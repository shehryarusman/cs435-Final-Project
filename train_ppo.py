import sys
import torch

from ppo import PPO
from network import FeedForwardNN
from game import Game
import numpy as np
import time

max_lives = 3
total_bullets = 4

def train(actor_model='', critic_model=''):
    state_space_size = 4
    action_space_size = 2
    game = Game()
    print(f"Training", flush=True)

    model = PPO(FeedForwardNN, game, action_space_size, state_space_size)
    
    if actor_model != '' and critic_model != '':
        print(f"Loading in {actor_model} and {critic_model}...", flush=True)
        model.actor.load_state_dict(torch.load(actor_model))
        model.critic.load_state_dict(torch.load(critic_model))
        print(f"Successfully loaded.", flush=True)
    elif actor_model != '' or critic_model != '': # Don't train from scratch if user accidentally forgets actor/critic model
        print(f"Error: Either specify both actor/critic models or none at all. We don't want to accidentally override anything!")
        sys.exit(0)
    else:
        print(f"Training from scratch.", flush=True)

    # model.learn(20)
    
    print("Testing")
    testing_player_wins = 0
    for i in range(100):
        game.reset()
        initial_state = game.get_initial_state()
        initial_state = np.array(initial_state, dtype=np.float64)
        curr_state = initial_state.reshape((1,4))


        while not game.is_over():
            action, _ = model.get_action(curr_state)
            reward, game_over, next_state = game.play_step(np.argmax(action))
            # print(f"Live Bullets: {game.bullets.count(1)} and Blank Bullets: {game.bullets.count(0)}")
            # print(f"Current State: Bullet Index {game.current_bullet_index}, Player Lives {game.player_lives}, Dealer Lives {game.dealer_lives}, Rounds {game.rounds}")
            # print(f"Agent Action: {'Shoot Dealer' if np.argmax(action) == 1 else 'Shoot Self'}")
            # print(f"Bullet was {'live' if game.bullets[game.current_bullet_index] else 'blank'}")
            # print("-" * 20)
            # time.sleep(2)
            # print(f"Dealer Action: {'Shoot Agent' if game.getDealerDecision() == 1 else 'Shoot Self'}")
            # print(f"Bullet was {'live' if game.bullets[game.current_bullet_index] else 'blank'}")
            # print(f"Player lives now {game.player_lives} and dealer lives now {game.dealer_lives}")
            # print(f"Reward: {reward}")
            # print("-" * 20)
            # time.sleep(2)
            
            if game_over:
                if game.player_lives > game.dealer_lives:
                    testing_player_wins += 1
                break
            
            curr_state = next_state
            curr_state = np.array(initial_state, dtype=np.float64)
            curr_state = initial_state.reshape((1,4))
            
            
    
    print(f"Testing Phase Wins: {testing_player_wins} ({(testing_player_wins/100)*100:.2f}%)")
    
    
if __name__ == "__main__":
    train('ppo_actor.pth', 'ppo_critic.pth')