# Prompt the user to enter the temperature in Fahrenheit
fahrenheit = float(input("Enter temperature in Fahrenheit: "))

# Convert the Fahrenheit temperature to Celsius
celsius = (fahrenheit - 32) * 5 / 9

# Output the temperature in Celsius
print("Temperature in Celsius: {:.2f}".format(celsius))
