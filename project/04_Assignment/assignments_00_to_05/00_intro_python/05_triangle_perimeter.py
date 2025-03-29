# Prompt the user to enter the lengths of each side of a triangle and then calculate and print the perimeter of the triangle (the sum of all of the side lengths).
# The program should perform the following tasks:
def main():
   side1 :float = float(input("Enter the length of side 1: "))
   side2 :float = float(input("Enter the length of side 2: "))
   side3 :float = float(input("Enter the length of side 3: "))
   print("The perimeter of the triangle is: ", side1 + side2 + side3)
if __name__ == '__main__':
    main()