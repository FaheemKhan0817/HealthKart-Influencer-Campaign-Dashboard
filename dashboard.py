import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -- Set up the page look and feel --
st.set_page_config(
    page_title="HealthKart Influencer Dashboard",
    page_icon="💪",
    layout="wide"
)

# -- Data loading with caching (handy for performance) --
@st.cache_data
def fetch_all_data():
    """
    Pulls together all influencer-related data from local CSVs.
    Slightly messy merge logic, but gets the job done.
    """
    try:
        inf_df = pd.read_csv("data/influencers.csv")
        posts_df = pd.read_csv("data/posts.csv")
        tracking_df = pd.read_csv("data/tracking_data.csv")
        payouts_df = pd.read_csv("data/payouts.csv")

        # Merge tracking + influencers
        combined_df = pd.merge(tracking_df, inf_df, left_on='influencer_id', right_on='id', how='left')

        # Only grab the bits we actually use from payouts to avoid field clashes
        slim_payouts = payouts_df[['influencer_id', 'basis', 'total_payout']]
        combined_df = pd.merge(combined_df, slim_payouts, on='influencer_id', how='left')

        # Handle date conversions early on so we don't mess this up later
        combined_df['date'] = pd.to_datetime(combined_df['date'])

        # Quick sanity check — this can be a lifesaver during debug
        expected_cols = ['orders', 'revenue', 'total_payout', 'platform', 'product', 'name', 'date']
        for key in expected_cols:
            if key not in combined_df.columns:
                st.error(f"Missing critical column: {key}. Check CSV schema?")
                return None, None, None, None, None

        return combined_df, inf_df, posts_df, tracking_df, payouts_df

    except FileNotFoundError as err:
        st.error(f"File not found: {err}. Make sure all CSVs are present.")
        return None, None, None, None, None

# Fetch everything up top
main_data, raw_influencers, raw_posts, raw_tracking, raw_payouts = fetch_all_data()

if main_data is not None:
    st.title("📈 HealthKart Influencer Campaign Dashboard")
    st.markdown("Easily explore how our influencers are doing and where the spend is going.")

    # Sidebar filters — these are actually super handy
    st.sidebar.header("Filter Dashboard")

    platforms = sorted(main_data["platform"].dropna().unique())
    products = sorted(main_data["product"].dropna().unique())
    categories = sorted(main_data["category"].dropna().unique())
    names = sorted(main_data["name"].dropna().unique())

    selected_plats = st.sidebar.multiselect("Platform", options=platforms, default=platforms)
    selected_prods = st.sidebar.multiselect("Product", options=products, default=products)
    selected_cats = st.sidebar.multiselect("Influencer Category", options=categories, default=categories)

    # Not doing influencer filter for now; gets messy quickly
    min_d = main_data["date"].min().date()
    max_d = main_data["date"].max().date()
    date_bounds = st.sidebar.date_input("Select Date Range", (min_d, max_d), min_value=min_d, max_value=max_d)

    # -- Filter logic block --
    if selected_plats and selected_prods and len(date_bounds) == 2:
        d1, d2 = date_bounds
        subset_df = main_data[
            (main_data["platform"].isin(selected_plats)) &
            (main_data["product"].isin(selected_prods)) &
            (main_data["category"].isin(selected_cats)) &
            (main_data["date"].dt.date >= d1) &
            (main_data["date"].dt.date <= d2)
        ]
    else:
        subset_df = pd.DataFrame()

    st.header("Campaign Performance Snapshot")

    # -- KPIs --
    if not subset_df.empty:
        total_rev = int(subset_df["revenue"].sum())
        total_orders = int(subset_df["orders"].sum())

        # Just grabbing one payout per influencer to avoid overcounting (was doing avg before—didn't work well)
        payout_totals = subset_df.groupby('influencer_id')['total_payout'].first()
        overall_payout = int(payout_totals.sum())

        # ROAS calc
        assumed_baseline = 0.15
        baseline_revenue = total_rev * assumed_baseline
        incremental_rev = total_rev - baseline_revenue

        # Avoid divide-by-zero
        roas = total_rev / overall_payout if overall_payout else 0
        inc_roas = incremental_rev / overall_payout if overall_payout else 0

        colA, colB, colC, colD = st.columns(4)
        colA.metric("Total Revenue", f"₹{total_rev:,.0f}")
        colB.metric("Total Payout", f"₹{overall_payout:,.0f}")
        colC.metric("ROAS", f"{roas:.2f}x", help="Revenue / Payout")
        colD.metric("Incremental ROAS", f"{inc_roas:.2f}x", help="Excludes estimated 15% organic rev")

    else:
        st.warning("No data for the current filter combo. Try tweaking the filters.")

    st.markdown("---")

    # -- Charts Zone --
    if not subset_df.empty:
        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("Revenue by Product")
            prod_rev = subset_df.groupby("product")["revenue"].sum().sort_values()
            fig1 = px.bar(
                prod_rev,
                x=prod_rev.values,
                y=prod_rev.index,
                orientation='h',
                title="Top Products",
                labels={"x": "Revenue", "y": "Product"},
                template="plotly_white"
            )
            st.plotly_chart(fig1, use_container_width=True)

        with col_right:
            st.subheader("Revenue by Platform")
            fig2 = px.pie(
                subset_df,
                names="platform",
                values="revenue",
                title="Platform Breakdown",
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            st.plotly_chart(fig2, use_container_width=True)

        # -- Influencer Tabs --
        st.header("Influencer Analysis")
        t1, t2, t3 = st.tabs(["🏆 Top Performers", "💸 Payout & ROI", "📊 Full Table"])

        with t1:
            st.subheader("Top 10 Influencers by Revenue")
            top_earners = subset_df.groupby(["name", "category"])["revenue"].sum().nlargest(10).reset_index()
            fig_top = px.bar(
                top_earners,
                x="revenue",
                y="name",
                color="category",
                orientation="h",
                title="Top Influencers"
            )
            fig_top.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_top, use_container_width=True)

        with t2:
            st.subheader("Payout vs. Revenue & ROAS")
            payout_vs_revenue = subset_df.groupby(['name','basis']).agg(
                total_revenue=('revenue', 'sum'),
                payout=('total_payout', 'first')
            ).reset_index()
            payout_vs_revenue['ROAS'] = payout_vs_revenue['total_revenue'] / payout_vs_revenue['payout']

            fig_scatter = px.scatter(
                payout_vs_revenue,
                x='payout',
                y='total_revenue',
                size='ROAS',
                color='basis',
                hover_name='name',
                size_max=50,
                labels={'payout': 'Total Payout (₹)', 'total_revenue': 'Total Revenue (₹)', 'basis': 'Payout Basis'},
                title="<b>Influencer ROI Analysis (Size of bubble = ROAS)</b>"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

        with t3:
            st.subheader("Full Influencer Dataset")

            detailed_view = subset_df.groupby(['name', 'platform', 'category', 'basis']).agg(
                Total_Revenue=('revenue', 'sum'),
                Total_Orders=('orders', 'sum'),
                Payout=('total_payout', 'first')
            ).reset_index()
            detailed_view['ROAS'] = (detailed_view['Total_Revenue'] / detailed_view['Payout']).round(2)

            st.dataframe(detailed_view.sort_values(by="Total_Revenue", ascending=False))

            # Exporter — may move to its own util later
            @st.cache_data
            def to_csv_bytes(df):
                return df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="📥 Download Summary CSV",
                data=to_csv_bytes(detailed_view),
                file_name="influencer_summary.csv",
                mime="text/csv"
            )
