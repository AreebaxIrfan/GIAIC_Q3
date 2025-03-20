#class-04
##Control Flow
#comparison Operator
#== ,!=, >,>= ,<=

x: int = 10
y: int = 20

print("x == y = ", x == y)
print("x != y = ", x != y)
print("x > y = ", x > y)
print("x >= y = ", x >= y)
print("x < y = ", x < y)

#Logical Operators

#The if Statement

if True:
    print("Hello")

#The else Statement

a = 10
if a == 10:
    print('hello')
else:
    print('world')

#The elif Statement

age= 18
if age> 18:
    print("you are eligiable for the student discount")
elif age < 18:
    print('Try next time')
else:
    print('Oops! Something went wrong')


#Nested if Statement
num : int = 10
if num > 0:
    if num % 2 == 0:
        print("The number is positive and even")
    else:
        print("The number is positive and odd")
else:
    print('the number is negative')

#List Tuple and Dictionary


#Lists 
fruites :list = ["apple", "banana", "cherry"]
numbers :list = [10 , 20 ,30 ,40]
mixed : list = ["hello" , 42 ,3.24, True]

print("fruites = ", fruites)
print("numbers =" ,  numbers)
print("mixed = " , mixed)

fruites: list = ['apple', 'banana' ,'cherry' ]
fruites[-3] = 'watermelon'
print(fruites)

# Tuples
tuple_1: tuple = tuple(["apple", "banana" ,"cherry"])
tuple_2: tuple = (10, 20, 30)
mixed_tuple : tuple = ("hello ", 42, 3.14 , True)

print('(tuple_1) = ', (tuple_1))
print('(tuple_2) ', (tuple_2))

tuple1: tuple = (10 ,20, 30)
tuple2: tuple = (10 ,20 ,30)

print("id(tuple1):", id(tuple1))
print("id(tuple2):" ,id(tuple2))

#Dictionary

thedict: dict = {
    "name":"Areeba Irfan",
    age:18,
    "country" :"Pakistan"
}
print("country")
print(thedict["name"])
#Set Data Types
my_set: set = {123, 454, 5,6}
my_set2: set = ([123,452,5,6])
unknown : set ={}
empty_set:set = set()

print(my_set)
print(my_set2)
print(type(my_set2))



my_Set : set = {1,2,3,4,5}
try:
    my_set[0]= 10
except TypeError as e:
    print (e)