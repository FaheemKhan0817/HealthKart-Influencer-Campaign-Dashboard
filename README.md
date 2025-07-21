# HealthKart Influencer Campaign Dashboard

This project is an interactive dashboard built with Streamlit to analyze and visualize the performance of HealthKart's influencer marketing campaigns. It provides at-a-glance metrics, performance deep-dives, and influencer-specific insights to enable data-driven decision-making.

## 🚀 Setup and Installation

Follow these steps to get the dashboard running on your local machine.

1.  **Prerequisites**:
    * Python 3.8+ installed.
    * `pip` (Python package installer).

2.  **Install Libraries**:
    Open your terminal and run the following command to install the necessary Python libraries:
    ```bash
    pip install streamlit pandas plotly
    ```

3.  **Data Files**:
    Ensure the following four data files are present in the same directory as the application script:
    * `influencers.csv`
    * `posts.csv`
    * `tracking_data.csv`
    * `payouts.csv`

4.  **Run the Application**:
    Navigate to the project directory in your terminal and execute:
    ```bash
    streamlit run your_script_name.py
    ```
    The dashboard will open in your web browser.

## 🧐 Key Assumptions

* **Data Attribution**: Revenue and orders in `tracking_data.csv` are accurately attributed to the correct influencer via reliable tracking methods (e.g., UTM codes, affiliate links).
* **Payouts**: The `total_payout` for each influencer is a fixed and final cost for the campaign period analyzed.
* **Incremental ROAS**: This metric is calculated by assuming a baseline organic revenue that would have occurred without the campaign. The dashboard assumes this baseline is **15% of the total generated revenue**. This percentage is a critical assumption and should be refined with historical data in a real-world scenario.

## ✨ Features

* **Performance Snapshot**: Key Performance Indicators (KPIs) like Total Revenue, Total Payout, Overall ROAS, and Incremental ROAS are displayed prominently.
* **Interactive Filtering**: The entire dashboard can be dynamically filtered by Platform, Product, and a specific Date Range.
* **Visual Analysis**:
    * Revenue breakdown by Product Category and Platform.
    * Bar chart identifying the Top 10 influencers by the revenue they generate.
* **Influencer Deep Dive**: Tab-based navigation to explore Top Performers, Payout & ROI Analysis, and view the full performance data table.
* **Data Export**: A download button allows users to export the summarized performance data to a CSV file for offline analysis.