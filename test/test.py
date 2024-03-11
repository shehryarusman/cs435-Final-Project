def battle(deck1, deck2):
    while len(deck1) > 0 and len(deck2) > 0:
        card1 = deck1.pop(0)
        card2 = deck2.pop(0)

        if card1 > card2:
            # Player 1 wins this battle
        elif card2 > card1:
            # Player 2 wins this battle
            deck2.extend([card2, card1])
        else:
            # A tie - War is declared
            print(f"Battle: Player 1 played {card1}")
            print(f"Battle: Player 2 played {card2}")
            print("Players tie on this battle. War is declared.")
            if not war(deck1, deck2, [card1, card2]):
                break  # If war returns False, it means one player cannot continue

    # Determine the winner
    if len(deck1) == 0:
        print("Player 2 is victorious!")
    else:
        print("Player 1 is victorious!")

def war(deck1, deck2, cards_in_war):
    # Ensure both players have enough cards for a war
    if len(deck1) < 2 or len(deck2) < 2:
        if len(deck1) > len(deck2):
            print("Player 2 does not have enough cards to continue. Player 1 is victorious!")
        else:
            print("Player 1 does not have enough cards to continue. Player 2 is victorious!")
        return False  # Indicates that the war could not be completed due to lack of cards

    # Each player places 1 card face down and 1 card face up
    face_down1, face_up1 = deck1.pop(0), deck1.pop(0)
    face_down2, face_up2 = deck2.pop(0), deck2.pop(0)

    # Add the face-down and face-up cards to the cards_in_war list
    cards_in_war.extend([face_down1, face_up1, face_down2, face_up2])

    print(f"War: Player 1 face down card: {face_down1}, face up card: {face_up1}")
    print(f"War: Player 2 face down card: {face_down2}, face up card: {face_up2}")

    if face_up1 > face_up2:
        # Player 1 wins the war
        deck1.extend(cards_in_war)
    elif face_up2 > face_up1:
        # Player 2 wins the war
        deck2.extend(cards_in_war)
    else:
        # Another tie - recursive war
        print("War: Another Tie. War is declared.")
        return war(deck1, deck2, cards_in_war)  # Recursive call with the current cards in war

    return True  # Indicates that the war was completed successfully

if __name__ == "__main__":
    print("Prepare for War (The Card Game).")
    d1 = [int(x) for x in input("Enter Player 1's cards from top to bottom, separated by spaces:\n").split()]
    d2 = [int(x) for x in input("Enter Player 2's cards from top to bottom, separated by spaces:\n").split()]

    if len(d1) != len(d2):
        print("Cannot play if decks have different numbers of cards.")
    else:
        battle(d1, d2)

