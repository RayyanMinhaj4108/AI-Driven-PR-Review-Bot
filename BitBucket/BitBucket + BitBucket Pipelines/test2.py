import random
import time

# Function to simulate a dice roll with optional delay for realism
def roll_dice(sides=6, delay=0):
    if sides < 2:
        raise ValueError("Dice must have at least 2 sides.")
    if delay:
        time.sleep(delay)  # Optional delay to simulate real dice rolling
    return random.randint(1, sides)

# Enhanced function with game rules, statistics, and optional custom dice
def play_game(player1, player2, rounds, sides=6, delay=0):
    if rounds < 1:
        raise ValueError("The number of rounds must be at least 1.")
    
    player1_score = 0
    player2_score = 0
    ties = 0

    for i in range(1, rounds + 1):
        roll1 = roll_dice(sides, delay)
        roll2 = roll_dice(sides, delay)

        print(f"Round {i}:")
        print(f"{player1} rolled: {roll1}")
        print(f"{player2} rolled: {roll2}")

        if roll1 > roll2:
            player1_score += 1
            print(f"{player1} wins this round!\n")
        elif roll2 > roll1:
            player2_score += 1
            print(f"{player2} wins this round!\n")
        else:
            ties += 1
            print("It's a tie!\n")

    print("\nFinal Results:")
    print(f"{player1}'s total score: {player1_score}")
    print(f"{player2}'s total score: {player2_score}")
    print(f"Ties: {ties}")

    if player1_score > player2_score:
        print(f"{player1} wins the game!")
    elif player2_score > player1_score:
        print(f"{player2} wins the game!")
    else:
        print("The game is a tie!")

# Example usage with 5 rounds and 6-sided dice, adding a slight delay between rolls
try:
    play_game("Alice", "Bob", 5, sides=6, delay=0.5)
except ValueError as e:
    print(f"Error: {e}")
