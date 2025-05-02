class TemperatureConverter:
    @staticmethod
    def celsius_to_fahrenheit(c):
        return round((c * 9/5) + 32 ,2)
    
celsius = 30
fahrenheit = TemperatureConverter.celsius_to_fahrenheit(celsius)
print(f"{celsius}°C is equal to {fahrenheit}°F")
