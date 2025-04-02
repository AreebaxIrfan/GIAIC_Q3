# Write a program which asks a user for their age and lets them know if they can or can't vote in the following three fictional countries.

PETURKSBOUIPO :int = 16
STANLAU_AGE :int = 25
MAYENGUA_AGE :int = 48

def main():
    user_age = int(input("How are you? "))

    if user_age >= PETURKSBOUIPO:
        print('You are vote in Peturksboupo where the voting age is ' + str(PETURKSBOUIPO) + '.')
    else:
        print("You cannot vote in Peturksbouipo where the voting age is "+ str(PETURKSBOUIPO) + '.')
    if user_age >= STANLAU_AGE:
        print('You can vote in Stanlu where the voting age is ' + str(STANLAU_AGE) + '.')
    else:
        print('You cannot vote in Stanlau where the votng age is ' + str(STANLAU_AGE)+ '.')
    if user_age >= MAYENGUA_AGE:
        print("You can vote in Mayengua where the voting age is " + str(MAYENGUA_AGE) + ".")
    else:
        print("You cannot vote in Mayengua where the voting age is " + str(MAYENGUA_AGE) + ".")


if __name__ == '__main__':
    main()