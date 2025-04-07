# There's a small fruit shop nearby your house that you like to buy from. Since you buy several fruit at a time, you want to keep track of how much the fruit will cost before you go. Luckily you wrote down what fruits were available and how much one of each fruit costs.

def main():
    fruits={
        'apple' : 1.5,
        'durian' : 50,
        'kiwi' : 1,
        'banana' : 2.5
    }

    total_cost = 0

    for fruites in fruits:
        price = fruits[fruites]
        amount_bought = int(input('How many (' + fruites + ") do you want to buy? "))
        total_cost += (price * amount_bought)
    print("Your total is $ " + str(total_cost))

if __name__ == '__main__':
    main()