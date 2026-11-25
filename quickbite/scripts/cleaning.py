
import pandas as pd
import re
import os

pd.options.display.float_format = '{:.2f}'.format
file_path = r"C:\Users\HP\Downloads\QuickBite\quickbite\data\QuickBite_Assessment.xlsx"

sheets = pd.read_excel(file_path, sheet_name=None)

cleaned_data = {}

for sheet_name in sheets:

    df = sheets[sheet_name]

    df.columns = df.columns.str.strip().str.lower()
    for col in df.select_dtypes(include=["object", "str"]).columns:
        df[col] = df[col].astype("string").str.strip()
        df[col] = df[col].replace("nan", pd.NA)
        df[col] = df[col].replace("", pd.NA)

    df = df.drop_duplicates()

    if sheet_name == "areas":

        df = df.dropna(subset=["area_id", "area_name", "city"])
        df = df.drop_duplicates(subset=["area_id"])
        df["city"] = df["city"].str.strip().str.title()

        df["city"] = df["city"].replace({
            "Blr": "Bengaluru",
            "Banglore": "Bengaluru",
            "Hyd": "Hyderabad",
            "Hydrabad": "Hyderabad",
            "Mum": "Mumbai",
            "Madras": "Chennai"
        })

        df["area_name"] = df["area_name"].str.title()


    elif sheet_name == "restaurants":

        df = df.dropna(subset=[
            "restaurant_id", "restaurant_name",
            "area_id", "cuisine", "onboard_date"
        ])

        df = df.drop_duplicates(subset=["restaurant_id"])

        df["onboard_date"] = pd.to_datetime(
            df["onboard_date"],
            format="mixed",
            errors="coerce",
            dayfirst=True
        )

        df = df.dropna(subset=["onboard_date"])

        df["restaurant_name"] = df["restaurant_name"].str.title()
        df["cuisine"] = df["cuisine"].str.title()

        df["rating"] = pd.to_numeric(
            df["rating"], errors="coerce"
        )

    # Delivery Partners
    elif sheet_name == "delivery_partners":

        df = df.dropna(subset=[
            "partner_id", "partner_name",
            "vehicle_type", "join_date"
        ])

        df = df.drop_duplicates(subset=["partner_id"])

        df["join_date"] = pd.to_datetime(
            df["join_date"],
            format="mixed",
            errors="coerce",
            dayfirst=True
        )

        df = df.dropna(subset=["join_date"])

        df["partner_name"] = df["partner_name"].str.title()

        df["vehicle_type"] = df["vehicle_type"].str.lower().str.strip()

        df["vehicle_type"] = df["vehicle_type"].replace({
            "bike": "Motorbike",
            "motor bike": "Motorbike",
            "motorbike": "Motorbike",
            "scooty": "Scooter",
            "activa": "Scooter",
            "scooter": "Scooter",
            "cycle": "Bicycle",
            "bicycle": "Bicycle",
            "ev": "Electric Vehicle",
            "e-scooter": "Electric Scooter",
            "ev scooter": "Electric Scooter"
        })

        df["vehicle_type"] = df["vehicle_type"].str.title()

    elif sheet_name == "customers":

        df = df.dropna(subset=[
            "customer_id", "customer_name", "signup_date"
        ])

        df = df.drop_duplicates(subset=["customer_id"])

        df["signup_date"] = pd.to_datetime(
            df["signup_date"],
            format="mixed",
            errors="coerce",
            dayfirst=True
        )

        df = df.dropna(subset=["signup_date"])

        df["customer_name"] = df["customer_name"].str.title()

        if "email" in df.columns:
            df["email"] = df["email"].str.lower()

    elif sheet_name == "orders":

        df = df.dropna(subset=[
            "order_id", "customer_id", "restaurant_id",
            "order_datetime", "order_amount",
            "payment_mode", "order_status"
        ])

        df = df.drop_duplicates(subset=["order_id"])

        df["order_datetime"] = pd.to_datetime(
            df["order_datetime"],
            format="mixed",
            errors="coerce",
            dayfirst=True
        )

        df["order_amount"] = df["order_amount"].astype("string")

        df["order_amount"] = df["order_amount"].str.replace(
            r'[^0-9.]', '', regex=True
        )

        df["order_amount"] = pd.to_numeric(
            df["order_amount"], errors="coerce"
        )
        df["delivery_minutes"] = df["delivery_minutes"].astype("string")

        df["delivery_minutes"] = df["delivery_minutes"].str.replace(
            r'[^0-9.]', '', regex=True
        )

        df["delivery_minutes"] = pd.to_numeric(
            df["delivery_minutes"], errors="coerce"
        )
        df["payment_mode"] = df["payment_mode"].str.lower().str.strip()

        df["payment_mode"] = df["payment_mode"].replace({
            "cash": "Cash on Delivery",
            "cod": "Cash on Delivery",
            "cash on delivery": "Cash on Delivery",
            "gpay": "UPI",
            "google pay": "UPI",
            "phonepe": "UPI",
            "upi": "UPI",
            "credit card": "Card",
            "debit card": "Card",
            "card": "Card"
        })

        df["payment_mode"] = df["payment_mode"].str.title()

        df["order_status"] = df["order_status"].str.lower().str.strip()

        df["order_status"] = df["order_status"].replace({
            "completed": "Delivered",
            "delivered": "Delivered",
            "canceled": "Cancelled",
            "cancelled": "Cancelled"
        })

        df["order_status"] = df["order_status"].str.title()

        df = df.dropna(subset=[
            "order_datetime", "order_amount"
        ])

        df["partner_id"] = df["partner_id"].fillna("Not Assigned")

        df["coupon_code"] = df["coupon_code"].fillna("No Coupon")

    elif sheet_name == "feedback":

        df = df.dropna(subset=[
            "feedback_id", "order_id", "rating", "feedback_date"
        ])

        df = df.drop_duplicates(subset=["feedback_id"])

        df["feedback_date"] = pd.to_datetime(
            df["feedback_date"],
            format="mixed",
            errors="coerce",
            dayfirst=True
        )

        df["rating"] = pd.to_numeric(
            df["rating"], errors="coerce"
        )

        df = df.dropna(subset=["feedback_date", "rating"])

        df["comment"] = df["comment"].fillna("No Comment")

    cleaned_data[sheet_name] = df


os.makedirs("cleaned_data", exist_ok=True)

with pd.ExcelWriter(
    "cleaned_data/Quick_Bite_Data_Cleaning.xlsx"
) as writer:

    for sheet_name in cleaned_data:

        df = cleaned_data[sheet_name]

        df.to_excel(
            writer,
            sheet_name=sheet_name,
            index=False
        )

df = cleaned_data["orders"]

df = df.merge(
    cleaned_data["customers"][["customer_id", "customer_name"]],
    on="customer_id",
    how="inner"
)

df = df.merge(
    cleaned_data["restaurants"][[
        "restaurant_id", "restaurant_name", "area_id", "cuisine"
    ]],
    on="restaurant_id",
    how="inner"
)

df = df.merge(
    cleaned_data["areas"][["area_id", "area_name", "city"]],
    on="area_id",
    how="left"
)

df = df.merge(
    cleaned_data["delivery_partners"][[
        "partner_id", "partner_name", "vehicle_type"
    ]],
    on="partner_id",
    how="left"
)

feedback_df = cleaned_data["feedback"].sort_values("feedback_date")

feedback_df = feedback_df.drop_duplicates(
    subset=["order_id"],
    keep="last"
)

df = df.merge(
    feedback_df[["order_id", "rating", "comment"]],
    on="order_id",
    how="left"
)

df["partner_name"] = df["partner_name"].fillna("Not Assigned")

df["vehicle_type"] = df["vehicle_type"].fillna("Not Available")

df["comment"] = df["comment"].fillna("No Comment")

df["order_date"] = df["order_datetime"].dt.strftime("%Y-%m-%d")

df["order_time"] = df["order_datetime"].dt.strftime("%H:%M:%S")

df["order_day"] = df["order_datetime"].dt.day_name()

df["is_late"] = df["delivery_minutes"].apply(
    lambda x: "Yes" if pd.notna(x) and x > 45 else "No"
)

columns = [
    "order_id",
    "order_date",
    "order_time",
    "order_day",
    "customer_name",
    "restaurant_name",
    "cuisine",
    "area_name",
    "city",
    "partner_name",
    "vehicle_type",
    "order_amount",
    "payment_mode",
    "coupon_code",
    "order_status",
    "delivery_minutes",
    "is_late",
    "rating",
    "comment"
]

df = df[columns]

df = df.sort_values("order_id")

df.to_excel(
    "cleaned_data/Quick_Bite_Combined_Data.xlsx",
    index=False
)


print("Cleaning completed")
print("Combined data created")
print("Total orders:", len(df))

print("\nMissing values in orders:")
print(cleaned_data["orders"].isnull().sum())

print("\nDelivery minutes:")
print(cleaned_data["orders"]["delivery_minutes"].head(15))

print("\nFirst five rows:")
print(df.head())
