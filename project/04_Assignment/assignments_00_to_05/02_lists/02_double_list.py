# Write a program that doubles each element in a list of numbers. For example, if you start with this list:

def main():
    numbers: list[int] = [1 ,2, 3, 4, 5]
    doubled_numbers: list[int] = []

    for number in numbers:
        doubled_numbers.append(number * 2)
    print("The doubled numbers are: ", doubled_numbers)

if __name__ == '__main__':
    main()