squares = []
for i in range(10):
    squares.append(i * i)   
squares = [i * i for i in range(10)]
print(squares)

even = [i for i in squares if i%2==0]
print(even)
pairs = [(x,y) for x in range(3) for y in range (2)]
print(pairs)
