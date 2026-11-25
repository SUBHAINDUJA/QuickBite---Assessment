import pandas as pd

pd.options.display.float_format = '{:.2f}'.format
import os

# Read the combined Excel file
df = pd.read_excel(r"C:\Users\HP\Downloads\QuickBite\quickbite\cleaned_data\Quick_Bite_Combined_Data.xlsx")

# Select delivered orders only
df["order_status"] = df["order_status"].astype(str).str.strip().str.title()
df = df[df["order_status"] == "Delivered"]

df["order_amount"] = pd.to_numeric(df["order_amount"], errors="coerce")
df["delivery_minutes"] = pd.to_numeric(df["delivery_minutes"], errors="coerce")
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

# 1. Area Performance
area = df.groupby(["area_name", "city"]).agg(
    total_orders=("order_id", "count"),
    revenue=("order_amount", "sum"),
    average_order_value=("order_amount", "mean"),
    average_delivery_minutes=("delivery_minutes", "mean"),
    average_rating=("rating", "mean")
).reset_index()

area = area.sort_values("revenue", ascending=False)
area["revenue_rank"] = range(1, len(area) + 1)
area[["revenue", "average_order_value", "average_delivery_minutes", "average_rating"]] = area[
    ["revenue", "average_order_value", "average_delivery_minutes", "average_rating"]
].round(2)

# 2. Top Cuisine by Day
cuisine = df.groupby(["order_day", "cuisine"]).size().reset_index(name="order_count")
day_total = df.groupby("order_day")["order_id"].count().reset_index(name="day_total_orders")
cuisine = cuisine.merge(day_total, on="order_day")
cuisine["share_percentage"] = (cuisine["order_count"] / cuisine["day_total_orders"]) * 100
cuisine = cuisine.sort_values(["order_day", "order_count"], ascending=[True, False])
cuisine = cuisine.drop_duplicates(subset=["order_day"])
cuisine["share_percentage"] = cuisine["share_percentage"].round(2)

# 3. Vehicle Performance
vehicle_df = df.dropna(subset=["vehicle_type"])
vehicle = vehicle_df.groupby("vehicle_type").agg(
    total_deliveries=("order_id", "count"),
    average_delivery_minutes=("delivery_minutes", "mean"),
    average_rating=("rating", "mean")
).reset_index()

vehicle["late_deliveries"] = vehicle_df[vehicle_df["delivery_minutes"] > 45].groupby(
    "vehicle_type"
)["order_id"].count().reindex(vehicle["vehicle_type"]).fillna(0).values

vehicle["late_percentage"] = (
    vehicle["late_deliveries"] / vehicle["total_deliveries"] * 100
).round(2)

vehicle = vehicle.sort_values("late_percentage")
vehicle[["average_delivery_minutes", "average_rating"]] = vehicle[
    ["average_delivery_minutes", "average_rating"]
].round(2)

# Save all results in one Excel file
os.makedirs(r"C:\Users\HP\Downloads\QuickBite\quickbite\analysis", exist_ok=True)

with pd.ExcelWriter(r"C:\Users\HP\Downloads\QuickBite\quickbite\analysis\Quick_Bite_Analysis.xlsx") as writer:
    area.to_excel(writer, sheet_name="Area Performance", index=False)
    cuisine.to_excel(writer, sheet_name="Top Cuisine by Day", index=False)
    vehicle.to_excel(writer, sheet_name="Vehicle Performance", index=False)

print("Analysis completed")
print("\nArea Performance")
print(area)
print("\nTop Cuisine by Day")
print(cuisine)
print("\nVehicle Performance")
print(vehicle)
