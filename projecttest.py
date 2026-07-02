import random

def roll():
    min_roll = 1
    max_roll = 6        
    roll=random.randint(min_roll, max_roll)
    return roll
while True:
    players=input("Enter the number of players: ")
    if players.isdigit():
        players=int(players)
        if 2<=players<=4:
            break
        else:
            print("Please enter a number between 2 and 4.")    
    else:
        print("Invalid input. Please enter a number.")
print(players)        

max_score = 100
player_scores = [0 for i in range(players)] 

print(player_scores)

while max(player_scores) < max_score:

    for player_idx in range(players):
        print(f"\nPlayer {player_idx + 1}'s turn:\n")
        current_score = 0

        while True:
            should_roll = input("Do you want to roll the dice? (y/n): ")
            if should_roll.lower() != 'y':
                break
       
            value = roll()
            if value == 1:
                print("You rolled a 1! You lose your turn. ")
                current_score = 0
                break
            else:
                current_score += value
                print("You rolled a: ", value)

            print("Your score is:\n", current_score)

        player_scores[player_idx] += current_score
        print("Your total score is: \n", player_scores[player_idx])
winning_idx=player_scores.index(max(player_scores))
print("Player", winning_idx + 1, "wins with a score of", player_scores[winning_idx], "!")