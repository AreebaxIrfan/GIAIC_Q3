#Lists and the Tuples and Dictionaries
#Lists
#A list is a collection which is ordered and changeable. In Python lists are written with square brackets.
#Create a List:
thislist = ["apple", "banana", "cherry"]
print(thislist)

#Access Items
#You access the list items by referring to the index number:
thislist = ["apple", "banana", "cherry"]
print(thislist[1])

#Tuple
#A tuple is a collection which is ordered and unchangeable. In Python tuples are written with round brackets.
#Create a Tuple:
thistuple = ("apple", "banana", "cherry")
print(thistuple)

#Access Tuple Items
#You can access tuple items by referring to the index number, inside square brackets:
print(thistuple[1])

#Change Tuple Values
#Once a tuple is created, you cannot change its values. Tuples are unchangeable, or immutable as it also is called.

#Dictionary
#A dictionary is a collection which is unordered, changeable and indexed. In Python dictionaries are written with curly brackets, and they have keys and values.
#Create and print a dictionary:
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
print(thisdict)

#Accessing Items
#You can access the items of a dictionary by referring to its key name, inside square brackets:
x = thisdict["model"]