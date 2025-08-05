

import math
def main():
    side_ab:float = float(input("Enter the length of AB: "))
    side_ac:float = float(input("Enter the length of AC: "))

    side_bc:float = math.sqrt(side_ab **2 + side_ac **2)
    print("The length of BC (the hypotenuse) is: ", str(side_bc))

# This provided line is required at the end of
# Python file to call the main() function.
if __name__ == '__main__':
    main()
