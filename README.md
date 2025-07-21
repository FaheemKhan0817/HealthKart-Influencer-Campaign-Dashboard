# 💪 HealthKart Influencer Campaign Dashboard

An interactive Streamlit dashboard designed to analyze and visualize the performance of HealthKart's influencer marketing campaigns. It delivers real-time insights, KPIs, and influencer-level ROI to empower data-driven decisions.

🔗 **[Launch the Live App 🚀](https://faheemkhan0817-healthkart-influencer-campaign--dashboard-x5oyfz.streamlit.app/)**

---

## 🎬 Demo Video

![Demo](asset/demo.gif)

> 📁 Local file path: `asset/demo.gif`


---

## ⚙️ Setup & Installation

Follow these steps to get the dashboard running locally:

### 1. Prerequisites
- Python 3.8+
- pip (Python package manager)

### 2. Install Required Libraries
```bash
pip install -r requirements.txt
```

### 3. Data Files
Make sure these data files are in the `/data` directory:
- `data/influencers.csv`
- `data/posts.csv`
- `data/tracking_data.csv`
- `data/payouts.csv`

### 4. Run the Application
```bash
streamlit run dashboard.py
```
The dashboard will launch automatically in your browser.

---

## 🧐 Key Assumptions

- **Data Attribution**: Orders and revenue in `tracking_data.csv` are assumed to be correctly mapped to influencers using UTM codes or affiliate links.
- **Payout Finality**: Each influencer’s `total_payout` is fixed and final for the given campaign period.
- **Incremental ROAS**: A baseline organic revenue of **15% of the total generated revenue** is assumed. This figure should ideally be adjusted using historical benchmarks in real-world deployments.

---

## ✨ Dashboard Features

- **📊 Performance Snapshot**  
  KPIs like **Total Revenue**, **Total Payout**, **Overall ROAS**, and **Incremental ROAS** at a glance.

- **🔍 Interactive Filters**  
  Filter results by:
  - Platform
  - Product
  - Date Range

- **📈 Visual Analytics**
  - Revenue breakdown by Product Category and Platform
  - Bar chart for **Top 10 influencers** by revenue

- **🔎 Influencer Deep Dive**
  - Tabbed views: Top Performers, ROI Analysis, Full Data Table

- **📤 Data Export**
  - Export summarized performance as CSV

---

## 📂 Project Structure

```plaintext
HealthKart-Influencer-Campaign-Dashboard/
├── asset/
│   └── video-demo.mp4
├── data/
│   ├── influencers.csv
│   ├── payouts.csv
│   ├── posts.csv
│   └── tracking_data.csv
├── dashboard.py
├── HealthKart_Influencer_Campaign_Dashboard.pdf
├── README.md
└── requirements.txt
```

---

## 🙌 Contributing

Feel free to fork the repository, raise issues, or contribute enhancements!

---