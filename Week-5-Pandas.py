#1
import pandas as pd

data = {
    "actor_id": [1, 1, 1, 1, 1, 2, 2],
    "director_id": [1, 1, 1, 2, 2, 1, 1],
    "timestamp": [0, 1, 2, 3, 4, 5, 6]
}
df = pd.DataFrame(data)

result = (
    df.groupby(["actor_id", "director_id"])
      .size()
      .reset_index(name="count")
      .query("count >= 3")[["actor_id", "director_id"]]
)
print(result)

#2 
data = {
    "user_id": [1, 2],
    "name": ["aLice", "bOB"]
}
df = pd.DataFrame(data)

df["name"] = df["name"].str.capitalize()

result = df.sort_values("user_id")

print(result)

#3
import pandas as pd

person = pd.DataFrame({
    "personId": [1, 2],
    "lastName": ["Wang", "Alice"],
    "firstName": ["Allen", "Bob"]
})

address = pd.DataFrame({
    "addressId": [1, 2],
    "personId": [2, 3],
    "city": ["New York City", "Leetcode"],
    "state": ["New York", "California"]
})

result = pd.merge(
    person,
    address[["personId", "city", "state"]],
    on="personId",
    how="left"
)

result = result[["firstName", "lastName", "city", "state"]]

print(result)

#4
employee = pd.DataFrame({
    "id": [1, 2, 3],
    "salary": [100, 200, 300]
})

salaries = employee["salary"].drop_duplicates().sort_values(ascending=False)

second_highest = salaries.iloc[1] if len(salaries) >= 2 else None

result = pd.DataFrame({"SecondHighestSalary": [second_highest]})

print(result)

#5
products = pd.DataFrame({
    "product_id": [1, 2, 3, 4, 5],
    "product_name": ["Leetcode Solutions", "Jewels of Stringology", "HP", "Lenovo", "Leetcode Kit"],
    "product_category": ["Book", "Book", "Laptop", "Laptop", "T-shirt"]
})

orders = pd.DataFrame({
    "product_id": [1,1,2,2,3,3,4,4,4,5,5,5],
    "order_date": pd.to_datetime([
        "2020-02-05","2020-02-10","2020-01-18","2020-02-11",
        "2020-02-17","2020-02-24","2020-03-01","2020-03-04","2020-03-04",
        "2020-02-25","2020-02-27","2020-03-01"
    ]),
    "unit": [60,70,30,80,2,3,20,30,60,50,50,50]
})

feb_orders = orders[
    (orders["order_date"].dt.year == 2020) &
    (orders["order_date"].dt.month == 2)
]

agg = feb_orders.groupby("product_id", as_index=False)["unit"].sum()

agg = agg[agg["unit"] >= 100]

result = agg.merge(products[["product_id", "product_name"]], on="product_id")[["product_name", "unit"]]

print(result)

#6
employees = pd.DataFrame({
    "id": [1, 7, 11, 90, 3],
    "name": ["Alice", "Bob", "Meir", "Winston", "Jonathan"]
})

employee_uni = pd.DataFrame({
    "id": [3, 11, 90],
    "unique_id": [1, 2, 3]
})

result = pd.merge(
    employees,
    employee_uni,
    on="id",
    how="left"
)

result = result[["unique_id", "name"]]

print(result)

#7
activity = pd.DataFrame({
    "player_id": [1, 1, 2, 3, 3],
    "device_id": [2, 2, 3, 1, 4],
    "event_date": pd.to_datetime([
        "2016-03-01", "2016-03-02", "2017-06-25", "2016-03-02", "2018-07-03"
    ]),
    "games_played": [5, 6, 1, 0, 5]
})

first_login = activity.groupby("player_id")["event_date"].min().reset_index()
first_login.rename(columns={"event_date": "first_login"}, inplace=True)

merged = activity.merge(first_login, on="player_id")
merged["is_next_day"] = merged["event_date"] == (merged["first_login"] + pd.Timedelta(days=1))

players_with_next_day = merged.groupby("player_id")["is_next_day"].any().sum()

total_players = first_login["player_id"].nunique()

fraction = round(players_with_next_day / total_players, 2)

result = pd.DataFrame({"fraction": [fraction]})
print(result)

#8
import pandas as pd

project = pd.DataFrame({
    "project_id": [1, 1, 1, 2, 2],
    "employee_id": [1, 2, 3, 1, 4]
})

employee = pd.DataFrame({
    "employee_id": [1, 2, 3, 4],
    "name": ["Khaled", "Ali", "John", "Doe"],
    "experience_years": [3, 2, 1, 2]
})

merged = project.merge(employee, on="employee_id")

result = merged.groupby("project_id")["experience_years"].mean().round(2).reset_index()

result.rename(columns={"experience_years": "average_years"}, inplace=True)

print(result)

#9
import pandas as pd

employee = pd.DataFrame({
    "id": [1, 2, 3, 4, 5, 6, 7],
    "name": ["Joe", "Henry", "Sam", "Max", "Janet", "Randy", "Will"],
    "salary": [85000, 80000, 60000, 90000, 69000, 85000, 70000],
    "departmentId": [1, 2, 2, 1, 1, 1, 1]
})

department = pd.DataFrame({
    "id": [1, 2],
    "name": ["IT", "Sales"]
})

merged = employee.merge(department, left_on="departmentId", right_on="id", suffixes=("", "_dept"))

merged["rnk"] = merged.groupby("departmentId")["salary"].rank(method="dense", ascending=False)

result = merged[merged["rnk"] <= 3][["name_dept", "name", "salary"]]

result.rename(columns={"name_dept": "Department", "name": "Employee", "salary": "Salary"}, inplace=True)

print(result)
