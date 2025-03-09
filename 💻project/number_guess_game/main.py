# import randdm module
import random

print("""
Welcome to the Number Guessing Game!
You got 5 try to guess the number between 50 to 100.
      """)

number = random.randrange(50, 100)
# chances to be given to the user to guess the number
chances= 5

guess_counter = 0
#using the while loop to run the game 

while guess_counter < chances:
    guess_counter += 1
    my_guess = int(input("Enter your guess: "))
    
    if my_guess == number:
        print(f"Congratulations! You have guessed the number in {guess_counter} tries.")
        break
    
    elif guess_counter >= chances and my_guess != number:
        print(f"Oops sorry! the number is {number} better luck next time.")
        
    elif my_guess < number :
        print("Your guess was very low , try again.")
    
    elif my_guess > number:
        print("Your guess very high, try again.")

