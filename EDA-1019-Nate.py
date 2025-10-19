import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# 1. Load dataset
# =========================
df = pd.read_csv("sentimentdataset.csv", encoding="utf-8")

# =========================
# 2. Basic inspection + Cleaning
# =========================
print("\nStep 2: Basic inspection of dataset")
print("Shape of dataset:", df.shape)
print("\nColumn info:")
print(df.info())
print("\nFirst five rows:")
print(df.head())

# --- Clean Platform ---
print("\nCleaning Platform column...")
df["Platform"] = df["Platform"].astype(str).str.strip()                 # Remove leading/trailing spaces
df["Platform"] = df["Platform"].str.replace(r"\s+", " ", regex=True)    # Replace multiple spaces with single space
df["Platform"] = df["Platform"].str.title()                             # Standardize case
print("Unique platforms after cleaning:", df["Platform"].unique())

# --- Clean Country ---
print("\nCleaning Country column...")
df["Country"] = df["Country"].astype(str).str.strip()                   # Remove leading/trailing spaces
df["Country"] = df["Country"].str.replace(r"\s+", " ", regex=True)      # Replace multiple spaces with single space
df["Country"] = df["Country"].str.title()                               # Standardize case

# Map variations to standardized names
country_mapping = {
    "Usa": "USA",
    "U.S.": "USA",
    "United States": "USA",
    "United States Of America": "USA",
    "Uk": "United Kingdom",
    "U.K.": "United Kingdom",
    "England": "United Kingdom",
    "Korea": "South Korea"
}
df["Country"] = df["Country"].replace(country_mapping)

print("Unique countries after cleaning:", df["Country"].unique()[:20])

# =========================
# 3. Simplify Sentiments into Positive / Neutral / Negative
# =========================
print("\nStep 3: Simplifying sentiments into Positive / Neutral / Negative")

sentiment_categories = {
    "Positive": [
        "Positive", "Happiness", "Joy", "Love", "Amusement", "Enjoyment",
        "Admiration", "Affection", "Awe", "Surprise", "Acceptance",
        "Adoration", "Anticipation", "Calmness", "Excitement", "Kind",
        "Pride", "Elation", "Euphoria", "Contentment", "Serenity",
        "Gratitude", "Hope", "Empowerment", "Compassion", "Tenderness",
        "Enthusiasm", "Fulfillment", "Reverence", "Zest", "Hopeful",
        "Proud", "Grateful", "Empathetic", "Compassionate", "Playful",
        "Inspired", "Confident", "Optimism", "Positivity", "Kindness",
        "Friendship", "Success", "Satisfaction", "Triumph", "Heartwarming"
    ],
    "Neutral": [
        "Neutral", "Confusion", "Indifference", "Curiosity", "Ambivalence",
        "Reflection", "Contemplation", "Acceptance", "Serenity", "Calmness"
    ],
    "Negative": [
        "Negative", "Anger", "Fear", "Sadness", "Disgust", "Disappointed",
        "Bitter", "Shame", "Despair", "Grief", "Loneliness", "Jealousy",
        "Resentment", "Frustration", "Boredom", "Anxiety", "Intimidation",
        "Helplessness", "Envy", "Regret", "Melancholy", "Nostalgia",
        "Yearning", "Fearful", "Apprehensive", "Overwhelmed", "Devastated",
        "Dismissive", "Heartbreak", "Betrayal", "Suffering", "Loss",
        "Isolation", "Exhaustion", "Sorrow", "Darkness", "Desperation",
        "Ruins", "Desolation", "Hate", "Bad", "Sad"
    ]
}

# Create a table of sentiment categories
df_sentiments = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in sentiment_categories.items()]))
print("\nSentiment Categories Table:")
print(df_sentiments)

# Function to simplify sentiment
def simplify_sentiment(s):
    s = str(s).strip()
    if s in sentiment_categories["Positive"]:
        return "Positive"
    elif s in sentiment_categories["Neutral"]:
        return "Neutral"
    else:
        return "Negative"

df["SentimentSimple"] = df["Sentiment"].apply(simplify_sentiment)
print("Unique simplified sentiments:", df["SentimentSimple"].unique())

# =========================
# 4. Sentiment Distribution
# =========================
print("\nStep 4: Sentiment Distribution (Positive / Neutral / Negative)")

sentiment_order = ["Positive", "Neutral", "Negative"]
sentiment_palette = {"Positive": "orange", "Neutral": "skyblue", "Negative": "lightgreen"}

plt.figure(figsize=(6,6))
sns.countplot(
    x="SentimentSimple",
    data=df,
    order=sentiment_order,
    palette=[sentiment_palette[s] for s in sentiment_order]
)
plt.title("Sentiment Distribution (3 categories)")
plt.show()

# =========================
# 5. Platform Distribution
# =========================
print("\nStep 5: Platform Distribution (with simplified sentiments)")

plt.figure(figsize=(8,6))
sns.countplot(x="Platform", hue="SentimentSimple", data=df,
              order=df["Platform"].value_counts().index)
plt.title("Platform Distribution by Sentiment (3 categories)")
plt.xticks(rotation=45, ha="right")
plt.show()

# =========================
# 6. Sentiment by Country (Top 10 countries)
# =========================
print("\nStep 6: Sentiment by Country (Top 10 countries, simplified sentiments)")

top_countries = df["Country"].value_counts().nlargest(10).index
plt.figure(figsize=(12,6))
sns.countplot(x="Country", hue="SentimentSimple",
              data=df[df["Country"].isin(top_countries)],
              order=top_countries)
plt.title("Top 10 Countries by Sentiment (3 categories)")
plt.xticks(rotation=45, ha="right")
plt.show()

# =========================
# 7. Engagement Analysis
# =========================
print("\nStep 7: Engagement Analysis (Retweets vs Likes, simplified sentiments)")

plt.figure(figsize=(6,6))
sns.scatterplot(x="Retweets", y="Likes", hue="SentimentSimple", data=df)
plt.title("Engagement: Retweets vs Likes (3 categories)")
plt.show()

# =========================
# 8. Yearly Sentiment Trend
# =========================

print("\nStep 8: Yearly Sentiment Trend (Positive / Neutral / Negative)")

# Convert timestamp to datetime and extract year
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df["Year"] = df["Timestamp"].dt.year

# Group by year and sentiment
yearly_sentiment = df.groupby(["Year","SentimentSimple"]).size().unstack(fill_value=0)

# Ensure index covers all years up to 2023
all_years = pd.Index(range(yearly_sentiment.index.min(), 2024))  # include 2023
yearly_sentiment = yearly_sentiment.reindex(all_years, fill_value=0)

# Plot
ax = yearly_sentiment.plot(kind="line", figsize=(12,6),
                           color={"Positive":"orange","Neutral":"skyblue","Negative":"lightgreen"},
                           marker="o")
plt.title("Yearly Sentiment Trend (3 categories)")
plt.ylabel("Count")
plt.xlabel("Year")

# Force x-axis to stop at 2023
plt.xlim(yearly_sentiment.index.min(), 2023)

# Show every year tick from min to 2023
plt.xticks(range(yearly_sentiment.index.min(), 2024))

plt.show()


# =========================
# 9. Text Length Distribution
# =========================
print("\nStep 9: Text Length Distribution")

df["TextLength"] = df["Text"].astype(str).apply(len)
plt.figure(figsize=(8,6))
sns.histplot(df["TextLength"], bins=30, kde=True)
plt.title("Distribution of Text Length")
plt.show()

# =========================
# 10. Sentiment Proportion Pie Chart
# =========================
print("\nStep 10: Sentiment Proportion Pie Chart (Positive / Neutral / Negative)")

sentiment_counts = df["SentimentSimple"].value_counts()
plt.figure(figsize=(6,6))
plt.pie(sentiment_counts, labels=sentiment_counts.index,
        autopct="%1.1f%%", startangle=90, colors=["orange","skyblue","lightgreen"])
plt.title("Proportion of Sentiments (3 categories)")
plt.show()

# =========================
# 11. Engagement by Sentiment
# =========================
print("\nStep 11: Engagement by Sentiment (平均 Retweets / Likes)")

engagement_summary = df.groupby("SentimentSimple")[["Retweets", "Likes"]].mean().round(2)
print(engagement_summary)

plt.figure(figsize=(8,6))
engagement_summary.plot(kind="bar", figsize=(8,6), color=["skyblue","orange"])
plt.title("Average Engagement (Retweets & Likes) by Sentiment")
plt.ylabel("Average Count")
plt.xticks(rotation=0)
plt.show()

# =========================
# 12. Engagement Distribution by Sentiment
# =========================
print("\nStep 12: Engagement Distribution by Sentiment")

plt.figure(figsize=(12,6))
sns.boxplot(x="SentimentSimple", y="Likes", data=df, palette=sentiment_palette)
plt.title("Likes Distribution by Sentiment")
plt.show()

# =========================
# 13. Engagement Correlation by Sentiment
# =========================
print("\nStep 13: Engagement Correlation by Sentiment")

plt.figure(figsize=(8,6))
sns.scatterplot(x="Retweets", y="Likes", hue="SentimentSimple", data=df, alpha=0.6)
plt.title("Engagement Correlation (Retweets vs Likes) by Sentiment")
plt.show()


# =========================
# 14. Text Length by Sentiment
# =========================
print("\nStep 14: Text Length Distribution by Sentiment")

plt.figure(figsize=(10,6))
sns.boxplot(x="SentimentSimple", y="TextLength", data=df, palette=sentiment_palette)
plt.title("Text Length Distribution by Sentiment (Boxplot)")
plt.show()

plt.figure(figsize=(10,6))
sns.violinplot(x="SentimentSimple", y="TextLength", data=df, palette=sentiment_palette)
plt.title("Text Length Distribution by Sentiment (Violin Plot)")
plt.show()


# =========================
# 15. Text Length vs Engagement
# =========================
print("\nStep 15: Text Length vs Engagement (Likes / Retweets)")

plt.figure(figsize=(8,6))
sns.scatterplot(x="TextLength", y="Likes", hue="SentimentSimple", data=df, alpha=0.6)
plt.title("Text Length vs Likes by Sentiment")
plt.show()

plt.figure(figsize=(8,6))
sns.regplot(x="TextLength", y="Retweets", data=df, scatter_kws={"alpha":0.3})
plt.title("Text Length vs Retweets (with Regression Line)")
plt.show()


# =========================
# 16. Text Length Grouping
# =========================
print("\nStep 16: Sentiment Distribution by Text Length Group")


labels = ["0-50","51-100","101-200","201-500","500+"]
df["LengthGroup"] = pd.cut(df["TextLength"], bins=bins, labels=labels, right=False)

plt.figure(figsize=(10,6))
sns.countplot(x="LengthGroup", hue="SentimentSimple", data=df, palette=sentiment_palette)
plt.title("Sentiment Distribution by Text Length Group")
plt.show()


# =========================
# 17. Engagement by Text Length Group
# =========================
print("\nStep 17: Average Engagement by Text Length Group")

engagement_by_length = df.groupby("LengthGroup")[["Likes","Retweets"]].mean()

engagement_by_length.plot(kind="bar", figsize=(10,6))
plt.title("Average Engagement (Likes & Retweets) by Text Length Group")
plt.ylabel("Average Likes / Retweets")
plt.show()
