import pandas as pd
import streamlit as st

# Load the datasets
purchase_details_path = 'D:/DL_work/Purchase_deatils_converted.csv'
sales_details_path = 'D:/DL_work/saved_sales_csv.csv 12-50-23-663.csv'
stock_details_path = 'D:/DL_work/Stock_deatils_converted.csv'


# Read the CSV files
purchase_details_df = pd.read_csv(purchase_details_path)
sales_details_df = pd.read_csv(sales_details_path)
stock_details_df = pd.read_csv(stock_details_path)
st.markdown(
    """
    <style>
    .reportview-container h1 {
        font-size: 1px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Streamlit app
st.title("Inventory and Sales Analysis Dashboard")
st.header("Purchase Details")
st.dataframe(purchase_details_df.head())

st.header("Sales Details")
st.dataframe(sales_details_df.head())

st.header("Stock Details")
st.dataframe(stock_details_df.head())

# Check column names and a few entries to understand the structure
st.write("Sales Details Columns:", sales_details_df.columns)
st.write("Sample of 'Entry Date' column:", sales_details_df['Entry Date'].head())

# Attempt to convert 'Entry Date' to datetime, handling errors
if 'Entry Date' in sales_details_df.columns:
    try:
        # Specify the format or use dayfirst=True if dates are in DD/MM/YYYY format
        sales_details_df['Entry Date'] = pd.to_datetime(sales_details_df['Entry Date'], format='%d/%m/%Y', errors='coerce')
    except ValueError as e:
        st.error(f"Date conversion error: {e}")
    # Check if there are any NaT values in 'Entry Date'
    st.write("Entries with NaT in 'Entry Date':", sales_details_df[sales_details_df['Entry Date'].isna()])
else:
    st.error("Column 'Entry Date' not found in sales_details_df.")

# Calculate the percentage of stock sold
def calculate_percentage_sold(stock_df, sales_df):
    stock_df['Initial Stock'] = stock_df['Stock(Unit1)'].astype(float) + stock_df['Stock(Unit2)'].astype(float)
    sales_grouped = sales_df.groupby('Entry No.').agg({'Qty(Unit1)': 'sum'}).reset_index()
    stock_df = pd.merge(stock_df, sales_grouped, left_on="'Product'", right_on='Entry No.', how='left').rename(columns={'Qty(Unit1)': 'Total Sold'})
    stock_df['Total Sold'] = stock_df['Total Sold'].fillna(0)
    stock_df['Percentage Sold'] = (stock_df['Total Sold'] / stock_df['Initial Stock']) * 100
    return stock_df

stock_df = calculate_percentage_sold(stock_details_df, sales_details_df)

# Track the sales rate over time to estimate days to sell out
def calculate_days_to_sell_out(stock_df, sales_df):
    if 'Entry Date' in sales_df.columns and 'Qty(Unit1)' in sales_df.columns:
        sales_df['Entry Date'] = pd.to_datetime(sales_df['Entry Date'], errors='coerce')
        stock_df['Sales Rate'] = stock_df.apply(lambda row: sales_df[sales_df['Entry No.'] == row["'Product'"]]['Qty(Unit1)'].sum() / ((sales_df['Entry Date'].max() - row['Date']).days + 1), axis=1)
        stock_df['Days to Sell Out'] = (stock_df['Stock(Unit1)'].astype(float) / stock_df['Sales Rate']).fillna(0).astype(int)
        return stock_df

stock_df = calculate_days_to_sell_out(stock_df, sales_details_df)

# Aggregate sales data by week, month, and quarter and identify top-selling items
def best_selling_items(sales_df, freq):
    if 'Entry Date' in sales_df.columns and 'Qty(Unit1)' in sales_df.columns:
        sales_df['Entry Date'] = pd.to_datetime(sales_df['Entry Date'], errors='coerce')
        sales_df.set_index('Entry Date', inplace=True)
        resampled_sales = sales_df.resample(freq)['Qty(Unit1)'].sum()
        top_selling = resampled_sales.sort_values(ascending=False).head(10)
        return top_selling

weekly_best_selling = best_selling_items(sales_details_df, 'W')
monthly_best_selling = best_selling_items(sales_details_df, 'M')
quarterly_best_selling = best_selling_items(sales_details_df, 'Q')

# Track non-moving products and their aging quantities
def track_non_moving_products(stock_df, sales_df, days_threshold=30):
    if 'Entry Date' in sales_df.columns:
        sales_df['Entry Date'] = pd.to_datetime(sales_df['Entry Date'], errors='coerce')
        non_moving = stock_df[~stock_df["'Product'"].isin(sales_df[sales_df['Entry Date'] > (pd.Timestamp.now() - pd.Timedelta(days=days_threshold))]['Entry No.'])]
        non_moving['Days in Stock'] = (pd.Timestamp.now() - pd.to_datetime(non_moving['Entry Date'], errors='coerce')).dt.days.fillna(0).astype(int)
        return non_moving

non_moving_products = track_non_moving_products(stock_df, sales_details_df)

# Identify slow-moving sizes within specific categories
def identify_slow_moving_sizes(sales_df):
    if 'Category' in sales_df.columns and 'Size' in sales_df.columns:
        slow_moving = sales_df.groupby(['Category', 'Size']).agg({'Qty(Unit1)': 'sum'}).reset_index()
        slow_moving = slow_moving[slow_moving['Qty(Unit1)'] == 0]
        return slow_moving

slow_moving_sizes = identify_slow_moving_sizes(sales_details_df)

# Provide insights on variances and suggest strategies for improvement
def provide_insights(stock_df):
    stock_df['Variance'] = stock_df['Stock(Unit1)'].astype(float) - stock_df['Total Sold'].astype(float)
    high_variance = stock_df[stock_df['Variance'] > stock_df['Variance'].mean()]
    strategies = high_variance.apply(lambda row: "Consider promotions or discounts" if row['Variance'] > 0 else "Restock soon", axis=1)
    return high_variance, strategies

high_variance_products, strategies_for_improvement = provide_insights(stock_df)

# Analyze turnaround time for exchanges and returns to optimize processes
def analyze_turnaround_time(returns_df):
    if 'Return Date' in returns_df.columns and 'Entry Date' in returns_df.columns:
        returns_df['Return Date'] = pd.to_datetime(returns_df['Return Date'], errors='coerce')
        returns_df['Turnaround Time'] = (returns_df['Return Date'] - pd.to_datetime(returns_df['Entry Date'], errors='coerce')).dt.days
        avg_turnaround_time = returns_df['Turnaround Time'].mean()
        return avg_turnaround_time

# Assuming returns_df contains the required data for exchanges and returns
returns_df = sales_details_df  # Placeholder
avg_turnaround_time = analyze_turnaround_time(returns_df)

# Generate reports on rejected goods and returns for vendor feedback
def generate_reports(returns_df):
    if 'Status' in returns_df.columns:
        rejected_goods_report = returns_df[returns_df['Status'] == 'Rejected']
        return rejected_goods_report

rejected_goods_report = generate_reports(returns_df)

# Recommend which products from our stock to prioritize for online sales
def recommend_online_sales(stock_df):
    stock_df['Priority for Online Sales'] = stock_df['Total Sold'] > stock_df['Total Sold'].mean()
    return stock_df[stock_df['Priority for Online Sales']]

online_sales_recommendations = recommend_online_sales(stock_df)

# Identify unique products to enhance our online portfolio
def identify_unique_products(stock_df):
    unique_products = stock_df[stock_df['Stock(Unit1)'].astype(float) == 1]
    return unique_products

unique_products = identify_unique_products(stock_df)

# Identify the top 20% of products contributing to 80% of sales
def identify_top_20_percent_sales(stock_df):
    stock_df = stock_df.sort_values(by='Total Sold', ascending=False)
    stock_df['Cumulative Sales'] = stock_df['Total Sold'].cumsum()
    total_sales = stock_df['Total Sold'].sum()
    top_20_percent = stock_df[stock_df['Cumulative Sales'] <= 0.8 * total_sales]
    return top_20_percent

top_20_percent_sales = identify_top_20_percent_sales(stock_df)

# Suggest strategies to reduce inventory of low-performing items
def suggest_inventory_reduction(stock_df):
    low_performing = stock_df[stock_df['Total Sold'] < stock_df['Total Sold'].mean()]
    reduction_strategies = low_performing.apply(lambda row: "Consider clearance sale" if row['Total Sold'] == 0 else "Bundle with high-performing items", axis=1)
    return low_performing, reduction_strategies

low_performing_products, reduction_strategies = suggest_inventory_reduction(stock_df)



st.header("Purchase Details")
st.dataframe(purchase_details_df.head())

st.header("Sales Details")
st.dataframe(sales_details_df.head())

st.header("Stock Details")
st.dataframe(stock_details_df.head())

st.header("Stock Analysis")
st.dataframe(stock_df[['NameToDisplay', 'Percentage Sold', 'Days to Sell Out']])

# Notify when items reach 75% and 50% sold
st.header("Notification for Items Sold")
threshold_50 = stock_df[stock_df['Percentage Sold'] >= 50]
threshold_75 = stock_df[stock_df['Percentage Sold'] >= 75]

st.write("Items that reached 50% sold:")
st.dataframe(threshold_50[['NameToDisplay', 'Percentage Sold', 'Days to Sell Out']])

st.write("Items that reached 75% sold:")
st.dataframe(threshold_75[['NameToDisplay', 'Percentage Sold', 'Days to Sell Out']])

# Weekly, Monthly, and Quarterly Best-Selling Items
st.header("Best-Selling Items")

st.subheader("Weekly Best-Selling Items")
st.dataframe(weekly_best_selling)

st.subheader("Monthly Best-Selling Items")
st.dataframe(monthly_best_selling)

st.subheader("Quarterly Best-Selling Items")
st.dataframe(quarterly_best_selling)

# Non-Moving Products
st.header("Non-Moving Products and Their Aging Quantities")
st.dataframe(non_moving_products[['NameToDisplay', 'Days in Stock', 'Stock(Unit1)', 'Stock(Unit2)']])

# Slow-Moving Sizes
st.header("Slow-Moving Sizes Within Specific Categories")
st.dataframe(slow_moving_sizes)

# Insights on Variances and Strategies for Improvement
st.header("Insights on Variances and Strategies for Improvement")
st.dataframe(high_variance_products[['NameToDisplay', 'Variance']])
st.write(strategies_for_improvement)

# Turnaround Time for Exchanges and Returns
st.header("Turnaround Time for Exchanges and Returns")
st.write(f"Average Turnaround Time: {avg_turnaround_time:.2f} days")

# Reports on Rejected Goods and Returns
st.header("Reports on Rejected Goods and Returns")
st.dataframe(rejected_goods_report)

# Recommendations for Online Sales
st.header("Recommendations for Online Sales")
st.dataframe(online_sales_recommendations[['NameToDisplay', 'Total Sold']])

# Unique Products for Online Portfolio
st.header("Unique Products to Enhance Online Portfolio")
st.dataframe(unique_products[['NameToDisplay', 'Stock(Unit1)']])

# Top 20% Products Contributing to 80% of Sales
st.header("Top 20% of Products Contributing to 80% of Sales")
st.dataframe(top_20_percent_sales[['NameToDisplay', 'Total Sold', 'Cumulative Sales']])

# Strategies to Reduce Inventory of Low-Performing Items
st.header("Strategies to Reduce Inventory of Low-Performing Items")
st.dataframe(low_performing_products[['NameToDisplay', 'Total Sold']])
st.write(reduction_strategies)
