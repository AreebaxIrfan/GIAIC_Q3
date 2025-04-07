# Write a program which asks the user how tall they are and prints whether or not they're taller than a pre-specified minimum height.

MINIMUM_HEIGHT :int = 50
def main():
    height = float(input('Please enter your height: '))
    if height >= MINIMUM_HEIGHT:
        print('You are tall enough')
    else:
        print('You are not tall enough , May be next time!')

if __name__ == '__main__':
    main()