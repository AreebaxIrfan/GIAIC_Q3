# Simulate rolling two dice, and prints results of each roll as well as the total.
import random
NUM_SIDES = 6
def main():
    die1 :int = random.randint(1 , NUM_SIDES)
    die2 :int = random.randint(1 , NUM_SIDES)
    total :int = die1 + die2
    print("The Dice have", NUM_SIDES, "sides each")
    print("Die 1: ", die1)
    print("Die 2: ", die2)
    print("Total of two dice: ", total)

# This provided line is required at the end of
# Python file to call the main() function.
if __name__ == '__main__':
    main()