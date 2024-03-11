import random

class Game:
    def __init__(self, verbose=False):
        self.total_bullets = 4
        self.player_lives = 3
        self.dealer_lives = 3
        self.rounds = 0
        self.verbose = verbose
        self._generate_bullets(initial=True)
        self.dealerDecision = None
    def print_verbose(self, *args, **kwargs):
            if self.verbose:
                print("\n--------------------------------------------------")
                print(*args, **kwargs)
                print("--------------------------------------------------\n")

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
        self.print_verbose("Bullets shuffled with live and blanks")

    def reset(self):
        self.player_lives = 3
        self.dealer_lives = 3
        self._generate_bullets(initial=True)
        self.rounds = 0

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
        self.print_verbose(f"Dealer decision: {decision}")
        return int(decision)

    def getDealerDecision(self):
        self.dealerDecision = self.dealer_decision()
        self.print_verbose(f"Dealer's turn, decision made: {self.dealerDecision}")
        return self.dealerDecision

    def play_step(self, action):
        reward = 0
        game_over = False
        turn_again = False

        self.print_verbose(f"Player action: {'Shoot themselves' if action == 0 else 'Shoot the dealer'}")
        bullet_type = "live" if self.bullets[self.current_bullet_index] == 1 else "blank"
        self.print_verbose(f"Bullet fired was {bullet_type}")

        if self.bullets[self.current_bullet_index] == 1:  # Live bullet
            if action == 0:  # Player shoots themselves
                self.player_lives -= 1
                reward = -100  # Penalty for getting shot
            else:  # Player shoots the dealer
                self.dealer_lives -= 1
                reward = 100  # Reward for shooting the dealer
            self.current_bullet_index += 1
        else:  # Blank bullet
            if action == 0:  # Player shoots themselves
                turn_again = True
                reward = 5  # Small reward for taking the risk
            else:  # Player attempts to shoot the dealer but it's a blank
                reward = 10  # Reward for surviving
            self.current_bullet_index += 1

        if not turn_again:
            if self.current_bullet_index == len(self.bullets):
                self._generate_bullets()

            game_over = self.player_lives == 0 or self.dealer_lives == 0
            if not game_over:  # If game is not over, dealer takes a turn
                dealer_turn_again = True
                while dealer_turn_again and not game_over:
                    dealer_turn_again = False
                    dealer_decision = self.getDealerDecision()
                    bullet_type = "live" if self.bullets[self.current_bullet_index] == 1 else "blank"
                    self.print_verbose(f"Dealer bullet fired was {bullet_type}")

                    if self.bullets[self.current_bullet_index] == 1:  # Live bullet
                        if dealer_decision == 0:  # Dealer shoots themselves
                            self.dealer_lives -= 1
                        else:  # Dealer shoots the player
                            self.player_lives -= 1
                        dealer_turn_again = False
                    else:  # Blank bullet
                        if dealer_decision == 0:  # Dealer shoots themselves
                            dealer_turn_again = True
                    self.current_bullet_index += 1

                    if self.current_bullet_index == len(self.bullets):
                        self._generate_bullets()

                    game_over = self.player_lives == 0 or self.dealer_lives == 0

        if self.current_bullet_index == len(self.bullets):
            self._generate_bullets()

        live_bullets = sum(self.bullets[self.current_bullet_index:])
        blank_bullets = len(self.bullets) - self.current_bullet_index - live_bullets
        self.print_verbose(f"Live bullets remaining: {live_bullets}, Blank bullets remaining: {blank_bullets}")
        self.print_verbose(f"Your lives: {self.player_lives}, Dealer's lives: {self.dealer_lives}")

        next_state = (self.player_lives, self.dealer_lives, live_bullets, blank_bullets)

        return reward, game_over, next_state 

    def is_over(self):
        return self.player_lives == 0 or self.dealer_lives == 0
    
    def get_initial_state(self):
        live_bullets = sum(self.bullets)
        blank_bullets = len(self.bullets) - live_bullets
        return (self.player_lives, self.dealer_lives, live_bullets, blank_bullets)

def main():
    game = Game(verbose=True)
    print("Game started. You and the dealer have 3 lives each.\n")
    
    while not game.is_over():
        input("Press Enter to reveal bullets status...")
        bullets_status = f"Live Bullets: {game.bullets[game.current_bullet_index:].count(1)} and Blank Bullets: {game.bullets[game.current_bullet_index:].count(0)}"
        print("\n" + bullets_status + "\n")
        
        player_action = input("Your action (0 to shoot yourself, 1 to shoot the dealer): ")
        while player_action not in ["0", "1"]:
            print("Invalid action. Please type '0' to shoot yourself, '1' to shoot the dealer.")
            player_action = input("Your action (0 or 1): ")
        
        player_action = int(player_action)
        input("Press Enter to proceed with your action...")
        reward, game_over, _, turn_again = game.play_step(player_action)
        
        if game_over:
            winner = "You win!" if game.player_lives > 0 else "Dealer wins!"
            print(f"\nGame over. {winner}\n")
            break
        else:
            print(f"Round concluded. Reward: {reward}. Press Enter to continue to the next round...")
            input()

if __name__ == "__main__":
    main()
