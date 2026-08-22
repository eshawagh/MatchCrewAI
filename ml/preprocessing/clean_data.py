import pandas as pd

# Step 1: Load the raw dataset
df = pd.read_csv("data/studentdata.csv", sep="\t")

print("Original shape:", df.shape)
print(df.head())

# Step 2: Clean column names (remove extra spaces)
df.columns = df.columns.str.strip()

# Step 3: Split comma-separated columns into clean lists
def split_and_clean(cell):
    if pd.isna(cell):
        return []
    items = cell.split(",")
    cleaned = [item.strip() for item in items]
    return cleaned

df["Technical Skills"] = df["Technical Skills"].apply(split_and_clean)
df["Preferred Domain(s)"] = df["Preferred Domain(s)"].apply(split_and_clean)

# Step 4: Check for missing values
print("\nMissing values per column:")
print(df.isnull().sum())

# Step 5: Check for duplicate students (by email)
duplicates = df[df.duplicated(subset=["Email Address"], keep=False)]
print("\nDuplicate students found:", len(duplicates))

# Step 6: Save cleaned version
df.to_csv("data/students_clean.csv", index=False)
print("\nCleaned file saved to data/students_clean.csv")