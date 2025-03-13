#Sets and the Frozenset

#Sets are used to store multiple items in a single variable.
#A set is a collection which is both unordered and unindexed.
#Sets are written with curly brackets.
#Create a Set:
my_set = {"apple", "banana", "cherry"}
print(my_set)
#Note: Sets are unordered, so you cannot be sure in which order the items will appear.

#Access Items
#You cannot access items in a set by referring to an index or a key.
#But you can loop through the set items using a for loop, or ask if a specified value is present in a set, by using the in keyword.
#Change Items
#Once a set is created, you cannot change its items, but you can add new items.
#Add Items
#To add one item to a set use the add() method.
#To add more than one item to a set use the update() method.
#Add an item to a set, using the add() method:
my_set.pop("orange")
my_set.discard("cherry")
my_set.add("orange")
my_set.remove("orange")
print(my_set)

#Frozen Sets
#Frozen sets in Python are immutable objects that only support methods and operators that produce a result without affecting the frozen set or sets to which they are applied.
#While elements of a set can be modified at any time, elements of the frozen set remain the same after creation.

my_frozenset:frozenset = frozenset({"apple", "banana", "cherry"})
print(my_frozenset)
#my_frozenset.add("orange") #This will raise an error