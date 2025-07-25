def celsius_to_fahrenheit(celsius):
    return celsius * 9/5 + 32

def fahrenheit_to_kelvin(fahrenheit):
    return (fahrenheit - 32) * 5/9 + 273.15

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

celsius=int(input("Enter temperature: "))
temp = celsius_to_fahrenheit(celsius)
print(f"{celsius}°C = {temp:.2f}°F")

fahrenheit = int(input("Enter temperature: "))
temp = fahrenheit_to_kelvin(fahrenheit)
print(f"{fahrenheit}°F = {temp:.2f}°K")

kelvin = int(input("Enter temperature: "))
temp = kelvin_to_celsius(kelvin)
print(f"{kelvin}°K = {temp:.2f}°C")
