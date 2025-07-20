import pandas as pd
import random
import os

# ✅ Step 1: Load File Safely
input_path = "Karachi_rest.csv"
if not os.path.exists(input_path):
    raise FileNotFoundError(f"❌ File '{input_path}' not found. Please check the path or ensure it exists.")

df = pd.read_csv(input_path)

# 🔍 Step 2: Preview columns before cleaning
print("📦 Columns in file:", df.columns.tolist())

# 🔡 Step 3: Clean column names
df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace('"', '')

# ✅ Step 4: Try dropping only if column exists
required_cols = ["CompleteStoreName", "City"]
missing_cols = [col for col in required_cols if col not in df.columns]

if missing_cols:
    print(f"⚠️ Warning: Missing columns in file — {missing_cols}. Skipping dropna step.")
else:
    df.dropna(subset=required_cols, inplace=True)

# ✏️ Step 5: Rename columns safely if they exist
rename_map = {
    "CompleteStoreName": "RestaurantName",
    "AverageRating": "Rating",
    "Reviewers": "Reviews"
}
rename_valid = {k: v for k, v in rename_map.items() if k in df.columns}
df.rename(columns=rename_valid, inplace=True)

# 🍽️ Step 6: Generate dummy menu
def generate_dishes():
    sample_dishes = ["Biryani", "Burger", "Zinger", "Karahi", "Roll", "Pizza", "Nihari", "Broast", "Ice Cream"]
    dish_list = random.sample(sample_dishes, k=3)
    return "; ".join([f"{dish} - Rs.{random.randint(200, 1000)}" for dish in dish_list])

if "RestaurantName" in df.columns:
    df["Menu"] = df["RestaurantName"].apply(lambda x: generate_dishes())
else:
    print("❌ 'RestaurantName' column not found. Menu generation skipped.")

# 💾 Step 7: Save cleaned file
output_path = "Karachi_rest.csv"
df.to_csv(output_path, index=False)

print(f"✅ Cleaned file saved successfully as '{output_path}'")
