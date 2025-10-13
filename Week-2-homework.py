import numpy as np
import pandas as pd

#1
A = np.array([1, 2, 3, 6, 9])
B = np.array([3, 4, 5, 6, 7])

v_stacked = np.vstack((A, B))

h_stacked = np.hstack((A, B))
print("Question 1")
print("vertical stack:\n", v_stacked)
print("horizontal stack:\n", h_stacked)

#2
common = np.intersect1d(A, B)
print("Question 2")
print("common elements:", common)

#3
range_vals = A[(A >= 5) & (A <= 10)]
print("Question 3")
print("Values between 5 and 10:", range_vals)


#4
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
iris_2d = np.genfromtxt(url, delimiter=',', dtype='float', usecols=[0,1,2,3])

# Condition: petallength (3rd col, index 2) > 1.5 AND sepallength (1st col, index 0) < 5.0
filtered = iris_2d[(iris_2d[:,2] > 1.5) & (iris_2d[:,0] < 5.0)]

print("Question 4")
print("Filtered rows:\n", filtered[:5])  # show first 5 rows

#1 pandas


df = pd.read_csv('https://raw.githubusercontent.com/selva86/datasets/master/Cars93_miss.csv')

result = df.loc[::20, ['Manufacturer', 'Model', 'Type']]
print("Question 1")
print(result)

#2

df['Min.Price'] = df['Min.Price'].fillna(df['Min.Price'].mean())
df['Max.Price'] = df['Max.Price'].fillna(df['Max.Price'].mean())
print("Question 2")
print(df[['Min.Price', 'Max.Price']].head(10))



#3

df = pd.DataFrame(np.random.randint(10, 40, 60).reshape(-1, 4))
filtered = df[df.sum(axis=1) > 100]
print("Question 3")
print(filtered)
