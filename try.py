import pandas as pd

# Load the original housing dataset
df = pd.read_csv("USA Housing Dataset.csv")

# Select only the necessary columns
columns_needed = [
    'date',         # Sale date
    'price',        # Sale price
    'bedrooms',     # Number of bedrooms
    'bathrooms',    # Number of bathrooms
    'sqft_living',  # Interior living space (sqft)
    'floors',       # Number of floors
    'yr_built',     # Year built
    'street',       # Street address
    'city',         # City
    'statezip'      # State + Zip code
]

# Filter and create the cleaned dataframe
df_cleaned = df[columns_needed]

# Optionally drop rows with any missing values (depends on your use case)
df_cleaned = df_cleaned.dropna()

# Save the cleaned data to a new CSV file
df_cleaned.to_csv("cleaned_housing_data.csv", index=False)

print("✅ Cleaned dataset saved as 'cleaned_housing_data.csv'")
