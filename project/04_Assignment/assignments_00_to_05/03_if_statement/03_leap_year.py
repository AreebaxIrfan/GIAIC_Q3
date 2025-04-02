# Write a program that reads a year from the user and tells whether a given year is a leap year or not.
def main():

    leap_year = int(input('Please input a year: '))

    if leap_year % 4 == 0:
        if leap_year %100 == 0:
            if leap_year % 400 == 0:
                print("That's a leap year")
            else:
                print('Its not a leap year')
        else:
            print("That's a leap year")
    else:
        print("That is not a leap year")

if __name__ == '__main__':
    main()