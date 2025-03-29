# Write a program that continually reads in mass from the user and then outputs the equivalent energy using Einstein's mass-energy equivalence formula (E stands for energy, m stands for mass, and C is the speed of light:

# E = m * c**2

c : int =  299792458 # Speed of light in m/s
def main():
    main_in_kg :float = float(input("Enter mass in kg: "))
    energy_in_jules : float = main_in_kg * c ** 2

    print(" e = m C^2...")
    print("m =" + str(main_in_kg) + " kg")
    print("c =" + str(c) + " m/s")
    print("E =" + str(energy_in_jules) + " J")

# This provided line is required at the end of
# Python file to call the main() function.
if __name__ == '__main__':
    main()