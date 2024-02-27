import random
import time

class DealerIntelligence:
    def __init__(self):
        self.lives = 3
        self.last_bullet_live = False

    def DealerChoice(self, bullets_left):
        if bullets_left == 1:
            return "1" if self.last_bullet_live else "0"
        else:
            decision = random.choice(["1", "0"])
            return decision

class Player:
    def __init__(self):
        self.lives = 3 

class Game:
    def __init__(self):
        self.player = Player()
        self.dealer = DealerIntelligence()
        self.bullets = 4

    def start(self):
        print("Welcome to the Russian Roulette Game!")
        print("You and the dealer will take turns shooting.")
        print(f"Each player starts with {self.player.lives} lives and the dealer starts with {self.dealer.lives} lives.")
        print(f"There are {self.bullets} bullets in the chamber.")
        print("Let's begin!\n")

        round_num = 1
        total_rounds_played = 0

        while self.player.lives > 0 and self.dealer.lives > 0:
            print(f"\nRound {round_num}:")

            live_bullets = random.randint(1, self.bullets)
            blank_bullets = self.bullets - live_bullets
            print(f"There are {live_bullets} live bullets and {blank_bullets} blank bullets in the chamber.")
            bullets_info = ["1"] * live_bullets + ["0"] * blank_bullets
            random.shuffle(bullets_info)  

            while bullets_info:
                print("\nYour turn:")
                choice = input("Do you want to shoot yourself (0) or the dealer (1)? ").lower()
                if choice == '0':
                    print("You aim the gun at yourself...")
                    result = bullets_info.pop(0)
                    if result == "1":
                        print("Bang! You're shot!")
                        self.player.lives -= 1
                    else:
                        print("Click... The chamber is empty.")
                        # Check if it was a blank, if yes, give the player another turn
                        if bullets_info and bullets_info[0] == "0":
                            print("You shot a blank! You get to go again.")
                            continue
                elif choice == '1':
                    print("You aim the gun at the dealer...")
                    result = bullets_info.pop(0)
                    if result == "1":
                        print("Bang! The dealer is shot!")
                        self.dealer.lives -= 1
                        if self.dealer.lives == 0:
                            print("You win! The dealer is out of lives.")
                            break
                    else:
                        print("Click... The chamber is empty.")
                        print("The dealer survived.")
                        # Check if it was a blank, if yes, give the dealer another turn
                        if bullets_info and bullets_info[0] == "0":
                            print("Dealer shot a blank! Dealer gets to go again.")
                            continue
                else:
                    print("Invalid choice. Please choose '0' to shoot yourself or '1' to shoot the dealer.")

                print("Your remaining lives:", self.player.lives)
                print("Dealer's remaining lives:", self.dealer.lives)

                if self.player.lives == 0:
                    print("You're out of lives. Game over!")
                    break

                time.sleep(1)  # Pause before dealer's turn

                print("\nDealer's turn:")
                dealer_decision = self.dealer.DealerChoice(len(bullets_info))
                print("Dealer is making a decision...")
                time.sleep(1)  # Pause before revealing dealer's decision
                if dealer_decision == "1":
                    print("The dealer aims the gun at you...")
                    result = bullets_info.pop(0)
                    if result == "1":
                        print("Bang! You're shot!")
                        self.player.lives -= 1
                    else:
                        print("Click... The chamber is empty.")
                else:
                    print("The dealer points the gun at themselves...")
                    result = bullets_info.pop(0)
                    if result == "1":
                        print("Bang! The dealer is shot!")
                        self.dealer.lives -= 1
                        if self.dealer.lives == 0:
                            print("You win! The dealer is out of lives.")
                            break
                    else:
                        print("Click... The chamber is empty.")
                        print("The dealer survived.")
                        self.dealer.last_bullet_live = False
                        if len(bullets_info) == 1:
                            self.dealer.last_bullet_live = True

                print("Your remaining lives:", self.player.lives)
                print("Dealer's remaining lives:", self.dealer.lives)

            total_rounds_played += 1
            round_num += 1

        print("\nThank you for playing!")
        print(f"Total rounds played: {total_rounds_played}")

# Start the game
game = Game()
game.start()
