
# Exercise 1: Count vowels
word = input("Enter a word: ")
vowels = "aeiouAEIOU"
count = 0

for char in word:
    if char in vowels:
        count += 1

print("Number of vowels:", count)

# Exercise decent2: Print animals in uppercase
animals = ['tiger', 'elephant', 'monkey', 'zebra', 'panther']

for i in animals:
    print(i.upper())

# Exercise 3: Odd or even from 1 to 20
for i in range(1, 21):
    if i % 2 == 0:
        print(i, "is even")
    else:
        print(i, "is odd")

# Exercise 4: Palindrome check
text = input("Enter a string: ")

if text == text[::-1]:
    print("This is a palindrome")
else:
    print("This is not a palindrome")

# Exercise 5 (Optional): Sum of two integers
def sum_of_integers(a, b):
    return a + b

x = int(input("Enter the first integer: "))
y = int(input("Enter the second integer: "))

print("The sum is:", sum_of_integers(x, y))