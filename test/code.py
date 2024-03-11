#!/usr/bin python3

def battle(deck1, deck2):

    if len(deck1) == 0:
        print("Player 2 is victorious!")
        return
    elif len(deck2) == 0:
        print("Player 1 is victorious!")
        return

    card1, card2 = deck1[0], deck2[0]
    print(f"Battle: Player 1 played {card1}")
    print(f"Battle: Player 2 played {card2}")

    if card1 > card2:
        print("Player 1 won this battle.")
        deck1.pop(0)
        deck2.pop(0)
        deck1.append(card1)
        deck1.append(card2)
        battle(deck1, deck2)
    elif card2 > card1:
        print("Player 2 won this battle.")
        deck1.pop(0)
        deck2.pop(0)
        deck2.append(card1)
        deck2.append(card2)
        battle(deck1, deck2)
    else:
        print("Players tie on this battle.\nWar is declared.")
        handle_war(deck1, deck2)

def handle_war(deck1, deck2):

    card1, card2 = deck1[0], deck2[0]
    face_down1, face_up1 = deck1[1], deck1[2]
    face_down2, face_up2 = deck2[1], deck2[2]

    print(f"War: Player 1 face down card: {face_down1}")
    print(f"War: Player 2 face down card: {face_down2}")
    print(f"War: Player 1 face up card: {face_up1}")
    print(f"War: Player 2 face up card: {face_up2}")

    if card1 > card2 :
        print("War: Player 1 won this war")
    elif card2 > card1:
        print("War: Player 2 won this war")
    else:
        print("War: Another Tie. War is declared.")
        handle_war(deck1, deck2)

if __name__ == "__main__":
    print("Prepare for War (The Card Game).")
    d1 = input("Enter your cards from top to bottom. Put spaces between values.\n").split()
    for i in range(len(d1)):
        d1[i] = int(d1[i])
    d2 = input("Enter your cards from top to bottom. Put spaces between values.\n").split()
    for i in range(len(d2)):
        d2[i] = int(d2[i])
    if len(d1) != len(d2):
        print("Cannot play if decks have different numbers of cards.")
        exit
    else:
        print(f"Player 1 Deck: {d1}")
        print(f"Player 2 Deck: {d2}")  
    battle(d1, d2)
    print(f"After Battle: Player 1 Deck contains {d1}")
    print(f"After Battle: Player 2 Deck contains {d2}")

    if len(d1) == 0:
        print("Player 2 is victorious!")
    elif len(d2) == 0:
        print("Player 1 is victorious!")
