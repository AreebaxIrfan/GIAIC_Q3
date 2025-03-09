# # Class 01 Assignement all Data Types and Keywords
# # Date: 2025-02-25
# Data Type  :: 	Example
# int	         x = 10
# float      	 y = 3.14
# complex	     z = 2 + 3j
# str	         text = "Hello"
# list	         my_list = [1, 2, 3]
# tuple	         my_tuple = (1, 2, 3)
# range	         r = range(5)
# set	         my_set = {1, 2, 3}
# frozenset	     f_set = frozenset([1, 2, 3])
# dict	         person = {"name": "Alice"}
# bool	         is_python_fun = True
# bytes	         bytes = b'hello'
# bytearray	     ba = bytearray([65, 66, 67])
# memoryview	 mv = memoryview(b'hello')
# NoneType	     nothing = None

# Keywords            :: 	 Example
# Control Flow               if, elif, else, for, while, break
# Exception Handling         try, except, finally
# Function & Class         	 def, return
# Variable & Scope	         global, nonlocal
# Import & Modules	         import, from, as
# Object-Oriented (OOP)	     del, class, object, issubclass, isinstance

#Numeric Types :: int, float, complex
# int Type :: integer(choose a random number)
x = 25
print(type(x))  # <class 'int'>

x = 3.14
print(type(x))  # <class 'float'>

x = 2 + 3j
print(type(x))  # <class 'complex'>


#Sequence Types :: list, tuple, range
#str Type :: string (choose a random word or sentence)
text= "Areeba"
print(type(text))  # <class 'str'>

#list Type :: list (choose a random list)
my_list = [1, 2, 3, 'cake' , 'mango' ,5.5]
print(type(my_list))  # <class 'list'>

#in the list (.append , .remove , .pop , .clear , .copy , .count , .extend , .index , .insert , .reverse , .sort) methods are used !

#tuple Type :: tuple (choose a random tuple)
my_tuple = (1, 2, 3, 'cake' , 'mango')
print(type(my_tuple))  # <class 'tuple'>

#range Type :: range (choose a random range)
r = range(5)
print(type(r))  # <class 'range'>

#Set Types :: set, frozenset   
#set Type :: set (choose a random set)
my_set = {1, 2, 3, 'cake' , 'mango'}
print(type(my_set))  # <class 'set'>

#frozenset Type :: frozenset (choose a random frozenset)
f_set = frozenset([1, 2, 3, 'cake' , 'mango'])  
print(type(f_set))  # <class 'frozenset'>

#Mapping Type :: dict
#dict Type :: dict (choose a random dictionary)
person = {"name": "Sara", "age": 25}
print(type(person))  # <class 'dict'>

#Boolean Type :: bool
#bool Type :: bool (choose a random boolean)
is_python_fun = True
print(type(is_python_fun))  # <class 'bool'>

#Binary Types :: bytes, bytearray, memoryview
#bytes Type :: bytes (choose a random byte)
bytes = b'hello'
print(type(bytes))  # <class 'bytes'>

#bytearray Type :: bytearray (choose a random bytearray)
ba = bytearray([65, 66, 67])
print(type(ba))  # <class 'bytearray'>

#memoryview Type :: memoryview (choose a random memoryview)
mv = memoryview(b'hello')
print(type(mv))  # <class 'memoryview'>

#None Type :: None
#None Type :: None (write None)
nothing = None
print(type(nothing))  # <class 'NoneType'>
