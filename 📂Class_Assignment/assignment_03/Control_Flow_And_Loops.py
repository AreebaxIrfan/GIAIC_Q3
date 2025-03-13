#Control-flow-and-loops

age = int(input("Enter your age: "))
if age >= 18:
    print("You are eligible to vote")
else:
    print("You are not eligible to vote")

for i in range(5):
    print(f"Iteration {i}")

fruits = ["apple", "banana", "cherry"]
fruits.append("orange")
print(fruits)

my_set =[1, 2, 3, 4, 5]
my_set.add(6)
print(my_set)

# loop in list
scorces = [85 ,92, 88, 78, 90]

for score in scorces:
    if score > 90:
        print("A")
    elif score > 80:
        print("B")
    elif score > 70:
        print("C")
    else:
        print("F")

