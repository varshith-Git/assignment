# Inventory Management Dashboard

## Overview

The Inventory Management Dashboard is a Streamlit application designed to help businesses manage their inventory efficiently. It provides various functionalities to monitor sales, track non-moving products, identify best-selling items, and suggest strategies to reduce inventory of low-performing items.

## Features

1. **Notification for Items Reaching 75% and 50% Sold**:
   - Alerts when items reach 75% and 50% sold, including days to sell out.

2. **Identify Best-Selling Items**:
   - Identifies weekly, monthly, and quarterly best-selling items.

3. **Track Non-Moving Products**:
   - Tracks non-moving products and their aging quantities.

4. **Identify Slow-Moving Sizes**:
   - Identifies slow-moving sizes within specific categories.

5. **Provide Insights on Variances**:
   - Provides insights on variances and suggests strategies for improvement.

6. **Analyze Turnaround Time for Exchanges and Returns**:
   - Analyzes turnaround time for exchanges and returns to optimize processes.

7. **Generate Reports on Rejected Goods and Returns**:
   - Generates reports on rejected goods and returns for vendor feedback.

8. **Recommend Products for Online Sales**:
   - Recommends which products from stock to prioritize for online sales.

9. **Identify Unique Products**:
   - Identifies unique products to enhance the online portfolio.

10. **Identify Top Products Contributing to Sales**:
    - Identifies the top 20% of products contributing to 80% of sales.

11. **Suggest Strategies to Reduce Inventory of Low-Performing Items**:
    - Suggests strategies such as flat 30% off, sale day, and buy-one-get-one-free promotions.

## Installation

To run the Inventory Management Dashboard, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/varshith-Git/assignment.git
    cd assignment
    ```

2. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Place your CSV files in the directory**:
    Ensure you have the following CSV files in the root directory:
    - `Purchase_deatils_converted.csv`
    - `saved_sales_csv.csv`
    - `Stock_deatils_converted.csv`

4. **Run the Streamlit application**:
    ```bash
    streamlit run display.py
    ```

## Usage

Once the application is running, you can navigate through the functionalities using the sidebar. Each functionality provides insights and actionable information to help manage your inventory effectively.

### Functionality Descriptions

1. **Notify Item Sales**:
   - Displays items that have reached 75% and 50% sales threshold and estimates days to sell out.

2. **Identify Best-Selling Items**:
   - Shows best-selling items over different time periods (weekly, monthly, quarterly).

3. **Track Non-Moving Products**:
   - Lists products that haven't been sold and their quantities.

4. **Identify Slow-Moving Sizes**:
   - Identifies slow-moving sizes in specific categories.

5. **Provide Insights on Variances**:
   - Highlights variances between ordered and current stock, providing suggestions for improvement.

6. **Analyze Turnaround Time**:
   - Analyzes the turnaround time for exchanges and returns to improve efficiency.

7. **Generate Reports on Rejections**:
   - Generates detailed reports on rejected goods and returns.

8. **Recommend Products for Online Sales**:
   - Suggests products that should be prioritized for online sales based on their performance.

9. **Identify Unique Products**:
   - Identifies unique products to enhance the online portfolio.

10. **Identify Top Products**:
    - Lists the top 20% of products that contribute to 80% of total sales.

11. **Suggest Inventory Reduction Strategies**:
    - Suggests strategies such as flat 30% off, sale day, and buy-one-get-one-free to reduce inventory of low-performing items.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue if you have any suggestions or find any bugs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or support, please contact [varshith.gudur17@gmail.com].
