# Guess My Number
# I am thinking of a number between 0 and 99... Enter a guess: 50 Your guess is too high
import random
def main():

    secret_number = random.randint(1 , 99)

    print('I am thinking between 1 and 99...')

    guess= int (input('Enter a guess: '))

    while guess != secret_number:
        if guess < secret_number:
            print('You guess is too low')
        else:
            print('Your guess is too high')
        print()
        guess= int(input("Enter a new guess: "))

    print('Congrats! Th number was: '+ str(secret_number))

if __name__ == '__main__':
    main()