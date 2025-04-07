import random
def main ():
    # Guess My Number
    secret_number = random.randint(1 , 99)
    guess = int(input('Enter a number: '))
    while guess != secret_number:
        if guess < secret_number:
            print('Your guess is too low')
        else:
            print('Your guess is too high')
        print()
        guess = int(input('Enter a new guess: '))
    print('Congrats! The number was: ' + str(secret_number))

if __name__ == '__main__':
    main()