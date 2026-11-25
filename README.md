# QuickBite---Assessment.
QuickBite is a fast-growing food delivery app operating in Bengaluru, Hyderabad, Chennai and  Mumbai. Each month the operations team reviews which areas are growing, what customers are  ordering and how well deliveries are running. The data comes straight out of different systems,  so it has never been cleaned or joined together. 

# QuickBite Data Analysis

## Project overview
This project uses QuickBite order data to clean the records, combine the related tables, and study order and delivery performance.

## Dataset
The input file is `data/QuickBite_Assessment.xlsx`. It contains six sheets:

- areas
- restaurants
- delivery_partners
- customers
- orders
- feedback

## Python files
- `scripts/cleaning.py` - cleans the six sheets and creates the combined order file.
- `scripts/analysis.py` - creates area, cuisine-by-day, and vehicle performance reports.

## Cleaning steps
1. Read the Excel sheets using pandas.
2. Remove duplicate rows and duplicate ID values.
3. Remove rows that are missing important values.
4. Remove extra spaces from text.
5. Convert date columns into date format.
6. Clean the order amount by removing currency symbols and commas.
7. Convert amount, delivery time, and rating columns into numbers.
8. Standardize city, payment, order status, and vehicle names.
9. Join the order data with customer, restaurant, area, delivery partner, and feedback details.

## Problems found
These are the problems and how I handle it.
1. Extra spaces in column names and values - strip()
2. Duplicate records - drop_duplicates()
3. Missing mandatory IDs and fields	- dropna(subset=...)
4. Different city spellings - Mapping dictionary
5. Inconsistent vehicle names - Standardized vehicle categories
6. Different order status values - Converted Completed/Delivered and Canceled/Cancelled
7. Different date formats - pd.to_datetime()
8. Invalid date values - errors="coerce"
9. Currency symbols and unwanted characters in amounts - Regular expressions
10. Numeric values stored as text - pd.to_numeric()
11. Missing delivery partner information - "Not Assigned"
12. Orders without matching customer or restaurant records	Inner joins

## Analysis
The analysis uses delivered orders.

- **Area Performance:** compares order count, revenue, average order value, delivery time, and rating.
- **Top Cuisine by Day:** finds the most ordered cuisine for each weekday and its order share.
- **Vehicle Performance:** compares delivery count, average delivery time, rating, and late delivery percentage.

## How to run

Open a terminal in the `quickbite` folder.

```bash
python scripts/cleaning.py
```
Run the analysis program:

```bash
python scripts/analysis.py
```

## Output files
- `cleaned_data/Quick_Bite_Data_Cleaning.xlsx`
- `cleaned_data/Quick_Bite_Combined_Data.xlsx`
- `analysis/Quick_Bite_Analysis.xlsx`
