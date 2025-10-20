import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# Load dataset and normalize column names
# -------------------------------
df = pd.read_csv("Brooklyn_Bridge_Automated_Pedestrian_Counts_Demonstration_Project_20251014.csv")

# Normalize column names: lowercase, strip spaces, replace spaces with underscores
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

print("Columns after normalization:", df.columns.tolist())

# -------------------------------
# Convert datetime and extract features
# -------------------------------
# Use flexible parsing to avoid NaT issues
df['hour_beginning'] = pd.to_datetime(df['hour_beginning'], errors="coerce")

# Convert numeric columns
for col in ['pedestrians', 'towards_manhattan', 'towards_brooklyn']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Extract useful features
df['day_of_week'] = df['hour_beginning'].dt.day_name()
df['year'] = df['hour_beginning'].dt.year
df['hour'] = df['hour_beginning'].dt.hour

print("\nSample rows after preprocessing:")
print(df.head())

# -------------------------------
# 1. Weekday pedestrian counts (Mon–Fri)
# -------------------------------
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
weekday_df = df[df['day_of_week'].isin(weekdays)]
weekday_counts = weekday_df.groupby('day_of_week')['pedestrians'].sum().reindex(weekdays)

print("\nWeekday pedestrian totals:")
print(weekday_counts)

plt.figure(figsize=(8,5))
sns.lineplot(x=weekday_counts.index, y=weekday_counts.values, marker="o")
plt.title("Brooklyn Bridge Pedestrian Counts by Weekday")
plt.ylabel("Total Pedestrians")
plt.xlabel("Day of Week")
plt.show()

# -------------------------------
# 2. Pedestrian counts in 2019 by weather condition
# -------------------------------
df2019 = df[df['year'] == 2019]
weather_counts = df2019.groupby('weather_summary')['pedestrians'].sum().sort_values(ascending=False)

print("\n2019 pedestrian totals by weather:")
print(weather_counts)

plt.figure(figsize=(10,6))
sns.barplot(y=weather_counts.index, x=weather_counts.values, palette="viridis")
plt.title("Pedestrian Counts by Weather Condition (2019)")
plt.xlabel("Total Pedestrians")
plt.ylabel("Weather Summary")
plt.show()

# -------------------------------
# 3. Correlation matrix between weather and pedestrian counts
# -------------------------------
weather_encoded = pd.get_dummies(df2019['weather_summary'])
corr_df = pd.concat([df2019[['pedestrians']], weather_encoded], axis=1)
corr_matrix = corr_df.corr()

plt.figure(figsize=(12,8))
sns.heatmap(corr_matrix[['pedestrians']].sort_values(by='pedestrians', ascending=False),
            annot=True, cmap="coolwarm", cbar=False)
plt.title("Correlation of Weather Conditions with Pedestrian Counts (2019)")
plt.show()

# -------------------------------
# 4. Categorize time of day (Morning, Afternoon, Evening, Night)
# -------------------------------
def categorize_time(hour):
    if pd.isna(hour):
        return None
    if 6 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 18:
        return "Afternoon"
    elif 18 <= hour < 24:
        return "Evening"
    else:
        return "Night"

df['time_of_day'] = df['hour'].apply(categorize_time)

# Only keep the four main categories
time_activity = df.groupby('time_of_day')['pedestrians'].sum().reindex(
    ["Morning","Afternoon","Evening","Night"]
)

print("\nPedestrian totals by time of day:")
print(time_activity)

plt.figure(figsize=(7,5))
sns.barplot(x=time_activity.index, y=time_activity.values, palette="Set2", hue=time_activity.index, legend=False)
plt.title("Pedestrian Activity by Time of Day (Brooklyn Bridge)")
plt.ylabel("Total Pedestrians")
plt.xlabel("Time of Day")
plt.show()

# -------------------------------
# 5. Show only first 5 values of location1
# -------------------------------
print("\nSample Location1 values (first 5):")
print(df['location1'].head())