# Problem Statement
# Use Python to calculate the number of seconds in a year, and tell the user what the result is in a nice print statement that looks like this (of course the value 5 should be the calculated number instead):

day_per_year: int = 365
hours_per_day: int = 24
minutes_per_hour: int = 60
seconds_per_minute: int = 60

def main():
    print("There are "+ str(day_per_year * hours_per_day * minutes_per_hour * seconds_per_minute) + " seconds in a year")
   


# This provided line is required at the end of
# Python file to call the main() function.
if __name__ == '__main__':
    main()