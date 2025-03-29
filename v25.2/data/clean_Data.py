import pandas as pd  

# Load CSV
df = pd.read_csv("./data/option_data.csv")

df = df.loc[:, ~df.columns.str.contains("Unnamed")]
# Print column count to verify structure
print("Detected Columns:", len(df.columns))
print("Columns:", df.columns.tolist())  # Print actual column names

# Rename columns dynamically (modify if needed)
df.columns = [
    "CALLS", "PUTS", "OI_CALL", "CHNG_IN_OI_CALL", "VOLUME_CALL", "IV_CALL", "LTP_CALL", "CHNG_CALL",
    "BID_QTY_CALL", "BID_CALL", "ASK_CALL", "ASK_QTY_CALL", "STRIKE",
    "BID_QTY_PUT", "BID_PUT", "ASK_PUT", "ASK_QTY_PUT", "CHNG_PUT", "LTP_PUT",
    "IV_PUT", "VOLUME_PUT", "CHNG_IN_OI_PUT", "OI_PUT"
]  # Ensure this matches exactly 24 columns

# Convert numeric columns (excluding 'STRIKE' & non-numeric fields)
numeric_cols = [col for col in df.columns if col not in ["STRIKE", "CALLS", "PUTS"]]
df[numeric_cols] = df[numeric_cols].replace("-", "0")  # Replace "-" with 0
df[numeric_cols] = df[numeric_cols].replace(",", "", regex=True)  # Remove commas
df[numeric_cols] = df[numeric_cols].astype(float)  # Convert to float


# Print cleaned data preview
print(df.head())

# Save cleaned data
df.to_csv("./data/cleaned_option_data.csv", index=False)
