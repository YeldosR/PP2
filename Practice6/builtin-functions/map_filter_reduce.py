from functools import reduce

numbers = [1, 2, 3, 4, 5]


squared = list(map(lambda x: x**2, numbers))
print("Map (squared):", squared)

evens = list(filter(lambda x: x % 2 == 0, numbers))
print("Filter (evens):", evens)

total = reduce(lambda x, y: x + y, numbers)
print("Reduce (sum):", total)


value = "123"
print("Type before:", type(value))

value = int(value)
print("Type after:", type(value))