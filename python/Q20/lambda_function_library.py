#  explain each line of the code
# this square function works by taking a number x and returning its square
#  eg: square(4) will return 16
# the reverse function takes a string s and returns it reversed
# eg: reverse("hello") will return "olleh"
# filter_evens function takes a list lst and returns a new list containing only even numbers from lst
# eg: filter_evens([1, 2, 3, 4]) will return [2, 4]
square = lambda x: x*x
reverse = lambda s : s[::-1]
filter_evens = lambda lst: list(filter(lambda x: x%2 ==0,lst))
print(square(4))
print(reverse("hello"))
print(filter_evens([1, 2, 3, 4]))