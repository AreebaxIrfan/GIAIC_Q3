import random

NUM_SIDES = 6
def roll_dice ():
    """Simulate rolling two dice adn prints their total"""
    die1: int = random.randint(1 , NUM_SIDES)
    die2: int = random.randint(1 , NUM_SIDES)
    total: int = die1 + die2
    print("Total of two die", total)

def main():
    die1 : int = 10
    print("die n main() starts as: " + str(die1))
    roll_dice()
    roll_dice()
    roll_dice()
    print("die in main() is: "+ str(die1)) 

if __name__ == '__main__':
    main()