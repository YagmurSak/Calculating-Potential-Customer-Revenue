import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# Read persona.csv file
df = pd.read_csv("persona.csv")
df.head()

# Missing value check
df.isnull().sum()

# General statistical summary for outlier checking
df.describe()


# Check to detect abnormal values in the price (PRICE) column.
plt.figure(figsize=(8, 6))     # Adjust the chart size
sns.boxplot(x=df["PRICE"])     # Create boxplot by price column
plt.title("Fiyat Dağılımı Boxplot")
plt.show()

# Number of unique SOURCE and their frequencies
df["SOURCE"].nunique()
df["SOURCE"].value_counts()

# Number of unique price
df["PRICE"].nunique()

# Number of sales at each price
df["PRICE"].value_counts()

# Number of sales from each country
df["COUNTRY"].value_counts()

# Total price from sales by countries
df.groupby("COUNTRY").agg({"PRICE": "sum"})

# Number of sales by source type
df["SOURCE"].value_counts()

# Averages of price by countries
df.groupby("COUNTRY").agg({"PRICE": "mean"})

# Averages of price by source
df.groupby("SOURCE").agg({"PRICE": "mean"})

# Price averages in the COUNTRY-SOURCE breakdown
df.groupby(["COUNTRY", "SOURCE"]).agg({"PRICE": "mean"})

# Price averages in the COUNTRY-SOURCE-SEX-AGE breakdown (with prices decreasing order)
agg_df = df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"}).sort_values("PRICE", ascending=False)


# Convert the names in the index to variable names
agg_df.reset_index(inplace=True)
agg_df

# Convert the AGE variable to a categorical variable and add it to agg_df
agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], [10, 18, 25, 30, 40, 50, 60, 70],
                           labels=["10_18", "19_25", "26_30", "31_40", "41_50", "51_60", "61_70"])


# Define new level-based customers (personas) by combining the observations in the output,
# and adding them to the dataset as variables

agg_df["customers_level_based"] = [agg_df["COUNTRY"][index].upper() + "_" + agg_df["SOURCE"][index].upper() + "_" +
                                   agg_df["SEX"][index].upper() + "_" + agg_df["AGE_CAT"][index].upper() for index in
                                   agg_df.index]
agg_df

# Define new dataframe by using customers_level_based
agg_df_1 = agg_df.groupby("customers_level_based").agg({"PRICE": "mean"}).reset_index()
agg_df_1


# Segment new personas
agg_df_1["SEGMENT"] = pd.qcut(agg_df_1["PRICE"], 4, labels=["D", "C", "B", "A"])
agg_df_1


# Group by segments and get price mean, max, sum
agg_df_1.groupby("SEGMENT").agg({"PRICE": ["mean", "max", "sum"]})


def find_segment_and_revenue(country, source, sex, age):
    # Convert age to category
    if 10 <= age <= 18:
        age_cat = "10_18"
    elif 19 <= age <= 25:
        age_cat = "19_25"
    elif 26 <= age <= 30:
        age_cat = "26_30"
    elif 31 <= age <= 40:
        age_cat = "31_40"
    elif 41 <= age <= 50:
        age_cat = "41_50"
    elif 51 <= age <= 60:
        age_cat = "51_60"
    else:
        age_cat = "61_70"

    new_user = f"{country.upper()}_{source.upper()}_{sex.upper()}_{age_cat}"  # Define user segment

    segment_info = agg_df_1[agg_df_1["customers_level_based"] == new_user]    # Find the user's segment and income

    if segment_info.empty:
        return "No segment found for this user."
    else:
        segment = segment_info["SEGMENT"].values[0]
        revenue = segment_info["PRICE"].values[0]
        return f"The new user belongs to segment '{new_user}'. Segment: {segment}, Estimated Revenue: {revenue:.2f}."


# Using function for new user
find_segment_and_revenue("TUR", "ANDROID", "FEMALE", 35)

find_segment_and_revenue("FRA", "IOS", "FEMALE", 33)



















