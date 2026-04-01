"""
Comprehensive Orders Dashboard
============================
A production-ready analytics dashboard for e-commerce orders data.
Built with Streamlit, Plotly, and DuckDB.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import duckdb
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

# Page config
st.set_page_config(
    page_title="Orders Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1rem;
        color: #666;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 1.5rem;
        color: white;
        text-align: center;
    }
    .metric-card.green {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    .metric-card.orange {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .metric-card.blue {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    .stMetric {
        background: transparent !important;
    }
    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data(ttl=300)
def load_data():
    """Load data from DuckDB with caching."""
    conn = duckdb.connect("dbt-local-agent.duckdb")

    # Load all tables
    daily_orders = conn.execute(
        "SELECT * FROM fct_daily_orders ORDER BY order_date"
    ).fetchdf()
    customers = conn.execute(
        "SELECT * FROM fct_customers ORDER BY customer_id"
    ).fetchdf()
    orders = conn.execute("SELECT * FROM fct_orders ORDER BY order_date").fetchdf()
    revenue_by_state = conn.execute(
        "SELECT * FROM fct_revenue_by_state ORDER BY state, order_date"
    ).fetchdf()

    conn.close()

    # Convert timestamps - handle both datetime and epoch timestamps
    daily_orders["order_date"] = pd.to_datetime(daily_orders["order_date"])
    orders["order_date"] = pd.to_datetime(orders["order_date"])
    revenue_by_state["order_date"] = pd.to_datetime(revenue_by_state["order_date"])

    # Calculate KPIs
    kpis = {
        "total_orders": len(orders),
        "total_revenue": float(
            orders[orders["order_status"] == "completed"]["order_total"].sum()
        ),
        "total_customers": orders["customer_id"].nunique(),
        "avg_order_value": float(
            orders[orders["order_status"] == "completed"]["order_total"].mean()
        )
        if len(orders[orders["order_status"] == "completed"]) > 0
        else 0.0,
        "completed_orders": len(orders[orders["order_status"] == "completed"]),
        "pending_orders": len(orders[orders["order_status"] == "pending"]),
        "cancelled_orders": len(orders[orders["order_status"] == "cancelled"]),
        "completion_rate": (
            len(orders[orders["order_status"] == "completed"]) / len(orders) * 100
        )
        if len(orders) > 0
        else 0.0,
    }

    # State aggregation
    state_summary = (
        revenue_by_state.groupby("state")
        .agg({"total_revenue": "sum", "order_count": "sum", "unique_customers": "sum"})
        .reset_index()
    )

    # Customer segments
    segments = (
        customers.groupby("customer_segment")
        .agg({"customer_id": "count", "total_revenue": "sum"})
        .reset_index()
    )
    segments.columns = ["segment", "customers", "revenue"]

    return {
        "daily_orders": daily_orders,
        "customers": customers,
        "orders": orders,
        "revenue_by_state": revenue_by_state,
        "state_summary": state_summary,
        "segments": segments,
        "kpis": kpis,
    }


def create_metric_card(value, label, delta=None, color="blue"):
    """Create a styled metric card."""
    delta_str = (
        f"<p style='font-size: 0.9rem; opacity: 0.9; margin: 0;'>{delta}</p>"
        if delta
        else ""
    )
    st.markdown(
        f"""
    <div class="metric-card {color}">
        <h2 style="margin: 0; font-size: 2rem; font-weight: 700;">{value}</h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">{label}</p>
        {delta_str}
    </div>
    """,
        unsafe_allow_html=True,
    )


def main():
    # Header
    st.markdown(
        '<h1 class="main-header">📊 Orders Analytics Dashboard</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="sub-header">Real-time insights into your e-commerce performance</p>',
        unsafe_allow_html=True,
    )

    # Load data
    with st.spinner("Loading data..."):
        data = load_data()

    # Sidebar filters
    st.sidebar.header("Filters")

    # Date range filter
    date_min = data["daily_orders"]["order_date"].min()
    date_max = data["daily_orders"]["order_date"].max()
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(date_min.date(), date_max.date()),
        min_value=date_min.date(),
        max_value=date_max.date(),
    )

    # Handle single date selection
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = date_min.date(), date_max.date()

    # State filter
    all_states = ["All"] + sorted(data["state_summary"]["state"].unique().tolist())
    selected_state = st.sidebar.selectbox("State", all_states)

    # Apply filters
    mask = (data["daily_orders"]["order_date"] >= pd.Timestamp(start_date)) & (
        data["daily_orders"]["order_date"] <= pd.Timestamp(end_date)
    )
    filtered_daily = data["daily_orders"][mask].copy()

    if selected_state != "All":
        mask_state = data["revenue_by_state"]["state"] == selected_state
        filtered_state = data["revenue_by_state"][mask_state]
    else:
        filtered_state = data["revenue_by_state"]

    # ===== KPI ROW =====
    st.markdown("### Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        create_metric_card(
            f"${data['kpis']['total_revenue']:,.0f}",
            "Total Revenue",
            f"{data['kpis']['completed_orders']} completed orders",
            "green",
        )
    with col2:
        create_metric_card(
            f"{data['kpis']['total_orders']}",
            "Total Orders",
            f"{data['kpis']['total_customers']} unique customers",
            "blue",
        )
    with col3:
        create_metric_card(
            f"${data['kpis']['avg_order_value']:.2f}",
            "Avg Order Value",
            f"Completion rate: {data['kpis']['completion_rate']:.1f}%",
            "orange",
        )
    with col4:
        create_metric_card(
            f"{data['kpis']['total_customers']}",
            "Total Customers",
            f"{len(data['segments'])} segments",
            "blue",
        )

    st.markdown("---")

    # ===== CHARTS ROW 1 =====
    st.markdown("### Revenue & Orders Over Time")

    col1, col2 = st.columns([2, 1])

    with col1:
        # Revenue trend chart - combined area + bar for simplicity
        fig = go.Figure()

        # Revenue area chart
        fig.add_trace(
            go.Scatter(
                x=filtered_daily["order_date"],
                y=filtered_daily["total_revenue"],
                name="Revenue ($)",
                mode="lines+markers",
                fill="tozeroy",
                line=dict(color="#38ef7d", width=2),
                marker=dict(size=8),
            )
        )

        # Orders as annotations on bars
        for i, row in filtered_daily.iterrows():
            fig.add_annotation(
                x=row["order_date"],
                y=row["order_count"] + 0.3,
                text=f"{int(row['order_count'])}",
                showarrow=False,
                font=dict(size=10, color="#4facfe"),
            )

        fig.update_layout(
            title="",
            legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.8)"),
            hovermode="x unified",
            height=400,
            margin=dict(l=50, r=50, t=30, b=30),
            yaxis=dict(title="Revenue ($)"),
        )
        fig.update_xaxes(title_text="Date")

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Order status donut
        status_data = {
            "Status": ["Completed", "Pending", "Cancelled"],
            "Count": [
                data["kpis"]["completed_orders"],
                data["kpis"]["pending_orders"],
                data["kpis"]["cancelled_orders"],
            ],
            "Color": ["#38ef7d", "#f59e0b", "#ef4444"],
        }

        fig_pie = go.Figure(
            data=[
                go.Pie(
                    labels=status_data["Status"],
                    values=status_data["Count"],
                    hole=0.6,
                    marker=dict(colors=status_data["Color"]),
                    textinfo="label+percent",
                    textposition="outside",
                )
            ]
        )

        fig_pie.update_layout(
            title="Order Status",
            height=400,
            showlegend=False,
            margin=dict(l=50, r=50, t=50, b=30),
        )

        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # ===== CHARTS ROW 2 =====
    st.markdown("### Geographic & Segment Analysis")

    col1, col2 = st.columns([1, 1])

    with col1:
        # Revenue by state bar chart - using express for better color handling
        state_data = (
            data["state_summary"].sort_values("total_revenue", ascending=True).copy()
        )

        fig_state = px.bar(
            state_data,
            y="state",
            x="total_revenue",
            orientation="h",
            color="total_revenue",
            color_continuous_scale="Blues",
            labels={"state": "", "total_revenue": "Revenue ($)"},
            text=state_data["total_revenue"].apply(lambda x: f"${x:,.0f}"),
        )

        fig_state.update_layout(
            title="Revenue by State",
            height=350,
            showlegend=False,
            margin=dict(l=50, r=80, t=50, b=30),
        )
        fig_state.update_traces(textposition="outside")

        st.plotly_chart(fig_state, use_container_width=True)

    with col2:
        # Customer segments
        fig_segments = px.pie(
            data["segments"],
            values="customers",
            names="segment",
            hole=0.5,
            color="segment",
            color_discrete_map={
                "High Value": "#10b981",
                "Medium Value": "#3b82f6",
                "Low Value": "#f59e0b",
                "No Purchases": "#ef4444",
            },
            title="Customers by Segment",
        )

        fig_segments.update_layout(
            height=350,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2),
            margin=dict(l=50, r=50, t=50, b=60),
        )

        st.plotly_chart(fig_segments, use_container_width=True)

    st.markdown("---")

    # ===== DETAILED BREAKDOWN =====
    st.markdown("### Daily Order Details")

    # Order status breakdown
    col1, col2, col3 = st.columns(3)

    with col1:
        fig_completed = go.Figure()
        fig_completed.add_trace(
            go.Scatter(
                x=filtered_daily["order_date"],
                y=filtered_daily["completed_orders"],
                mode="lines+markers",
                fill="tozeroy",
                line=dict(color="#10b981", width=2),
                name="Completed",
                marker=dict(size=6),
            )
        )
        fig_completed.update_layout(
            title="Completed Orders",
            height=250,
            showlegend=False,
            margin=dict(l=30, r=30, t=40, b=30),
            xaxis_title="",
            yaxis_title="Orders",
        )
        st.plotly_chart(fig_completed, use_container_width=True)

    with col2:
        fig_pending = go.Figure()
        fig_pending.add_trace(
            go.Scatter(
                x=filtered_daily["order_date"],
                y=filtered_daily["pending_orders"],
                mode="lines+markers",
                fill="tozeroy",
                line=dict(color="#f59e0b", width=2),
                name="Pending",
                marker=dict(size=6),
            )
        )
        fig_pending.update_layout(
            title="Pending Orders",
            height=250,
            showlegend=False,
            margin=dict(l=30, r=30, t=40, b=30),
            xaxis_title="",
            yaxis_title="Orders",
        )
        st.plotly_chart(fig_pending, use_container_width=True)

    with col3:
        fig_cancelled = go.Figure()
        fig_cancelled.add_trace(
            go.Scatter(
                x=filtered_daily["order_date"],
                y=filtered_daily["cancelled_orders"],
                mode="lines+markers",
                fill="tozeroy",
                line=dict(color="#ef4444", width=2),
                name="Cancelled",
                marker=dict(size=6),
            )
        )
        fig_cancelled.update_layout(
            title="Cancelled Orders",
            height=250,
            showlegend=False,
            margin=dict(l=30, r=30, t=40, b=30),
            xaxis_title="",
            yaxis_title="Orders",
        )
        st.plotly_chart(fig_cancelled, use_container_width=True)

    st.markdown("---")

    # ===== DATA TABLES =====
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📍 Revenue by State")
        st.dataframe(
            data["state_summary"]
            .sort_values("total_revenue", ascending=False)
            .rename(
                columns={
                    "state": "State",
                    "total_revenue": "Revenue",
                    "order_count": "Orders",
                    "unique_customers": "Customers",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

    with col2:
        st.markdown("### 👥 Customer Segments")
        st.dataframe(
            data["segments"]
            .sort_values("revenue", ascending=False)
            .rename(
                columns={
                    "segment": "Segment",
                    "customers": "Customers",
                    "revenue": "Revenue",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("---")

    # ===== TOP CUSTOMERS =====
    st.markdown("### 🏆 Top Customers by Revenue")

    top_customers = data["customers"][
        [
            "customer_name",
            "email",
            "state",
            "total_orders",
            "total_revenue",
            "customer_segment",
        ]
    ].copy()
    top_customers = top_customers.sort_values("total_revenue", ascending=False).head(10)

    fig_top = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=[
                        "<b>Customer</b>",
                        "<b>Email</b>",
                        "<b>State</b>",
                        "<b>Orders</b>",
                        "<b>Revenue</b>",
                        "<b>Segment</b>",
                    ],
                    fill_color="#1a1a2e",
                    font=dict(color="white", size=12),
                    align="left",
                    height=35,
                ),
                cells=dict(
                    values=[
                        top_customers["customer_name"],
                        top_customers["email"],
                        top_customers["state"],
                        top_customers["total_orders"],
                        top_customers["total_revenue"].apply(lambda x: f"${x:,.2f}"),
                        top_customers["customer_segment"],
                    ],
                    fill_color="rgba(248, 250, 252, 0.5)",
                    align="left",
                    height=30,
                    font=dict(size=11),
                ),
            )
        ]
    )

    fig_top.update_layout(height=300, margin=dict(l=0, r=0, t=10, b=10))

    st.plotly_chart(fig_top, use_container_width=True)

    # Footer
    st.markdown("---")
    st.markdown(
        f"<p style='text-align: center; color: #666; font-size: 0.85rem;'>"
        f"📊 Dashboard generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
        f"Data source: DuckDB (dbt-local-agent)"
        f"</p>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
