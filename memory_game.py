import random

cards = ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D']

random.shuffle(cards)

# Create a list to keep track of which cards have been revealed
revealed = [False] * len(cards)

def display_board():
    for i in range(len(cards)):
        if revealed[i]:
            print(cards[i], end=' ')
        else:
            print('*', end=' ')
        if (i + 1) % 4 == 0:  # 4 cards per row
            print()

def get_choices():
    while True:
        try:
            choice1 = int(input("Pick the first card (1-8): ")) - 1
            choice2 = int(input("Pick the second card (1-8): ")) - 1

            # Validate choices
            if choice1 == choice2:
                print("You must pick two different cards!")
            elif not (0 <= choice1 < len(cards)) or not (0 <= choice2 < len(cards)):
                print("Invalid positions, pick numbers between 1 and 8!")
            elif revealed[choice1] or revealed[choice2]:
                print("One or both cards are already revealed. Try again!")
            else:
                return choice1, choice2
        except ValueError:
            print("Please enter numbers only!")

attempts = 0
matches_found = 0
total_matches = len(cards) // 2

while matches_found < total_matches:
    display_board()
    choice1, choice2 = get_choices()

    # Reveal chosen cards temporarily
    revealed[choice1] = True
    revealed[choice2] = True
    display_board()

    # Check if they match
    if cards[choice1] == cards[choice2]:
        print("It's a match! 🎉")
        matches_found += 1
    else:
        print("Not a match. Try again.")
        # Hide them again after showing
        revealed[choice1] = False
        revealed[choice2] = False

    attempts += 1
    input("Press Enter to continue...")  # Pause to let player see

print(f"Congratulations! You won in {attempts} attempts! 🏆")
