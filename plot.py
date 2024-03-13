import matplotlib.pyplot as plt

def plot_performance(total_rewards, exploration_rates, wins_per_episode):
    episodes = range(1, len(total_rewards) + 1)
    episodes2 = range(1, len(exploration_rates) + 1)
    episodes3 = range(1, len(wins_per_episode) + 1)

    fig, ax = plt.subplots(3, 1, figsize=(10, 15))

    # Plot total rewards per episode
    ax[0].plot(episodes, total_rewards, label='Total Rewards per Episode')
    ax[0].set_xlabel('Episodes')
    ax[0].set_ylabel('Total Rewards')
    ax[0].set_title('Agent\'s Performance Over Time')
    ax[0].legend()

    # Plot exploration rate decay
    ax[1].plot(episodes2, exploration_rates, label='Exploration Rate', color='r')
    ax[1].set_xlabel('Episodes')
    ax[1].set_ylabel('Exploration Rate')
    ax[1].set_title('Exploration Rate Decay')
    ax[1].legend()

    # Plot wins over episodes
    ax[2].plot(episodes3, wins_per_episode, label='Cumulative Wins', color='g')
    ax[2].set_xlabel('Episodes')
    ax[2].set_ylabel('Wins')
    ax[2].set_title('Cumulative Wins Over Episodes')
    ax[2].legend()

    plt.tight_layout()
    plt.show()
