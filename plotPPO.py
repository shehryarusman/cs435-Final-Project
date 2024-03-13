import matplotlib.pyplot as plt
import numpy as np

def plotPPO(testing_player_wins, rewards_per_game=None):
    games = list(range(1, 101)) 

    fig, ax1 = plt.subplots()

    # Plotting win counts
    color = 'tab:red'
    ax1.set_xlabel('Game')
    ax1.set_ylabel('Wins', color=color)
    ax1.plot(games, np.cumsum([1 if win else 0 for win in testing_player_wins]), color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    if rewards_per_game is not None:
        ax2 = ax1.twinx()  
        color = 'tab:blue'
        ax2.set_ylabel('Total Reward', color=color)  
        ax2.plot(games, rewards_per_game, color=color)
        ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  
    plt.title('PPO Agent Performance')
    plt.show()
