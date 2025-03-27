# Ask the user for a number and print its square (the product of the number times itself).

# Here's a sample run of the program (user input is in bold italics):

# Type a number to see its square: 4

# 4.0 squared is 16.0

def main():
    # Prompt the user to enter a number
    number :float = float(input("Type a numberto see its square: "))

    # Calculate the square of the number
    square : float = number * number

    print(f"{number} squared is {square}")

if __name__ == '__main__':
    main()