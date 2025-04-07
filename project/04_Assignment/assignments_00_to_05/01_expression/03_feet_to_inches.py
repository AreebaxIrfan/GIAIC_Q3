# Converts feet to inches. Feet is an American unit of measurement. There are 12 inches per foot. Foot is the singular, and feet is the plural
Feet_to_Inches :int = 20
def main():
    feet:float = float(input("Enter the number of feet: "))
    inches:float = feet * Feet_to_Inches
    print(f"{feet} feet is equal to {inches} inches")




# This provided line is required at the end of
# Python file to call the main() function.
if __name__ == '__main__':
    main()