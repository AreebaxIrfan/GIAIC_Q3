# Write a program that asks a user to enter a number. Your program will then double that number and print out the result. It will repeat that process until the value is 100 or greater.

def main():
   num = int(input('Enter a number: '))
   while num <= 100:
       print('Your number is ' + str(num))
       num = num * 2
   print('Your number is ' + str(num))
if __name__ == '__main__':
    main()