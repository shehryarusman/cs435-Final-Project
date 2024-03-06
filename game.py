import random

class Game:
    def __init__(self):
        self.total_bullets = 4
        self.player_lives = 3
        self.dealer_lives = 3
        self.rounds = 0
        self._generate_bullets()
        self.dealerDecision = None

    def _generate_bullets_ppo(self):
        live_bullets = random.randint(1, self.total_bullets)
        blank_bullets = self.total_bullets - live_bullets
        self.bullets = [1] * live_bullets + [0] * blank_bullets
        random.shuffle(self.bullets)
        self.current_bullet_index = 0
        self.rounds += 1
        
        return live_bullets, blank_bullets

    def _generate_bullets(self):
        live_bullets = random.randint(1, self.total_bullets)
        blank_bullets = self.total_bullets - live_bullets
        self.bullets = [1] * live_bullets + [0] * blank_bullets
        random.shuffle(self.bullets)
        self.current_bullet_index = 0
        self.rounds += 1

    def reset(self):
        self.player_lives = 3
        self.dealer_lives = 3
        self._generate_bullets()
        self.rounds = 0
        self.current_bullet_index = 0

    def reset_ppo(self):
        self.player_lives = 3
        self.dealer_lives = 3
        l, b = self._generate_bullets_ppo()
        self.rounds = 0
        self.current_bullet_index = 0
        
        return (self.player_lives,
            self.dealer_lives,
            l,
            b)

    def dealer_decision(self):
        if len(self.bullets) - self.current_bullet_index == 1:
            decision = "1" if not self.bullets[self.current_bullet_index] else "0"
        else:
            decision = random.choice(["1", "0"])
        return int(decision)

    def getDealerDecision(self):
        self.dealerDecision = self.dealer_decision()
        return self.dealerDecision

    def play_step(self, action):
        reward = 0
        game_over = False
        dealer_goes_again = False

        while True:
            if self.bullets[self.current_bullet_index] == 1:
                if action == 0:  # Player shoots themselves
                    self.player_lives -= 1
                    reward = -100  # Penalty for getting shot
                else:  # Player shoots the dealer
                    self.dealer_lives -= 1
                    reward = 100  # Reward for shooting the dealer
            else:  # Blank bullet
                reward = 10  # Reward for surviving
                if action == 0:  # Player shot themselves with a blank
                    break  # Player gets an additional turn

            self.current_bullet_index += 1
            if self.current_bullet_index == len(self.bullets):
                self._generate_bullets()  # Start a new round if all bullets are used

            game_over = self.player_lives == 0 or self.dealer_lives == 0
            if game_over or action == 1:  # If game is over or player chose to shoot the dealer, break the loop
                break

        if not game_over:  # Proceed with dealer's turn if game is not over
            dealer_goes_again = True
            while dealer_goes_again:
                dealer_goes_again = False  # Reset flag for each iteration
                dealerDecision = self.getDealerDecision()
                if self.bullets[self.current_bullet_index] == 1:  # Live bullet
                    if dealerDecision == 0:  # Dealer shoots themselves
                        self.dealer_lives -= 1
                    else:  # Dealer shoots the player
                        self.player_lives -= 1
                else:  # Blank bullet
                    if dealerDecision == 0:  # Dealer shot themselves with a blank
                        dealer_goes_again = True  # Dealer gets an additional turn

                self.current_bullet_index += 1
                if self.current_bullet_index == len(self.bullets):
                    self._generate_bullets()  # Start a new round if all bullets are used

                game_over = self.player_lives == 0 or self.dealer_lives == 0
                if game_over:
                    break  # Exit the loop if the game is over

        live_bullets = sum(self.bullets[self.current_bullet_index:])
        blank_bullets = len(self.bullets) - self.current_bullet_index - live_bullets

        next_state = (self.player_lives, self.dealer_lives, live_bullets, blank_bullets)

        return reward, game_over, next_state

    def is_over(self):
        return self.player_lives == 0 or self.dealer_lives == 0

    def get_initial_state(self):
            live_bullets = sum(self.bullets)
            blank_bullets = len(self.bullets) - live_bullets
            return (self.player_lives, self.dealer_lives, live_bullets, blank_bullets)
def main():
    game = Game()
    print("Game started. You and the dealer have 3 lives each.")
    print("Type '0' to shoot yourself, '1' to shoot the dealer.")
    
    while not game.is_over():
        print(f"\nRound {game.rounds}:")
        print(f"Player Lives: {game.player_lives}, Dealer Lives: {game.dealer_lives}")
        print(f"Live Bullets: {sum(game.bullets[game.current_bullet_index:])}, Blank Bullets: {len(game.bullets) - sum(game.bullets[game.current_bullet_index:])}")
        
        player_action = input("Your action (0 or 1): ")
        while player_action not in ["0", "1"]:
            print("Invalid action. Please type '0' to shoot yourself, '1' to shoot the dealer.")
            player_action = input("Your action (0 or 1): ")
        
        player_action = int(player_action)
        reward, game_over, _ = game.play_step(player_action)
        
        if game_over:
            print("Game Over")
            if game.player_lives == 0:
                print("You lost. Better luck next time!")
            else:
                print("Congratulations! You won!")
            break
        else:
            print(f"Round result: Reward {reward}, Player Lives: {game.player_lives}, Dealer Lives: {game.dealer_lives}")

if __name__ == "__main__":
    main()