# # Write a program to solve this age-related riddle!

# Anton, Beth, Chen, Drew, and Ethan are all friends. Their ages are as follows:

# Anton is 21 years old.

# Beth is 6 years older than Anton.

# Chen is 20 years older than Beth.

# Drew is as old as Chen's age plus Anton's age.

# # Ethan is the same age as Chen.

def main():
    # Constants for ages
    anton_age :int = 21
    beth_age :int = anton_age + 6
    chen_age :int = beth_age + 20
    drew_age :int = chen_age + anton_age
    ethan_age :int = chen_age

    print("Anton is", anton_age, "years old.")
    print("Beth is", beth_age, "years old.")
    print("Chen is", chen_age, "years old.")
    print("Drew is", drew_age, "years old.")
    print("Ethan is", ethan_age, "years old.")
# This provided line is required at the end of
# Python file to call the main() function.
if __name__ == '__main__':
    main()