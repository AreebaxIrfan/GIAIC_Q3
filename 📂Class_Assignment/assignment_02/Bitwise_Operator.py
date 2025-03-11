#Bitwise Operator
#Bitwise operator works on bits and performs bit by bit operation.
a = 10  # 1010 in binary
b = 4   # 0100 in binary

# Bitwise AND
result = a & b
print("Bitwise AND:", result)  # Output: 0

# Bitwise OR
result = a | b
print("Bitwise OR:", result)  # Output: 14

# Bitwise XOR
result = a ^ b
print("Bitwise XOR:", result)  # Output: 14

# Bitwise NOT
result = ~a
print("Bitwise NOT:", result)  # Output: -11

# Bitwise left shift
result = a << 2
print("Bitwise left shift:", result)  # Output: 40

# Bitwise right shift
result = a >> 2
print("Bitwise right shift:", result)  # Output: 2