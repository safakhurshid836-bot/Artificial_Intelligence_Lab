def get_correct_value(number):
    if number % 3 == 0 and number % 5 == 0:
        return "Fizz Buzz" 
    elif number % 3 == 0:
        return "Fizz" 
    elif number % 5 == 0:
        return "Buzz" 
    else:
        return str(number)


print(">>> Fizz Buzz Game <<<")
print(f'Game Rules:')
print(f'If number is divisible by 3 and 5, then say "FIZZ BUZZ".')
print(f'If number is divisible by 3 only, then say "FIZZ".')
print(f'If number is divisible by 5 only, then say "BUZZ".')
print(f'Otherwise say the number instead.')

player1 = input("Name of Player 1: ")
player2 = input("Name of Player 2: ")

print(f'NOTE: In this game capitaliza the first letter!')

players_list = [player1, player2]
current_player_index = 0

# to print the 100 rounds
for number in range(1, 101):
    
    current_player = players_list[current_player_index]
    print(f'Number: {number}')
    user_input = input(f"{current_player}'s turn: ").strip()
    
    correct_answer = get_correct_value(number)
    
    # if any player enter wrong answer
    if user_input != correct_answer:
        print(f'Your Answer is Wrong!')
        print(f'Correct answer was: {correct_answer}')
        print(f'{players_list[1 - current_player_index]} wins!')
        print(f'Thanks for playing this game!')
        break
    
    # To switch the player (0 → 1, 1 → 0)
    current_player_index = 1 - current_player_index

else:
    print(f'Both players completed all 100 rounds successfully!')
    print(f'Thanks for playing this game!')