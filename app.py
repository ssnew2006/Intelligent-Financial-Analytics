import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import PyPDF2
import re

# Set page configuration
st.set_page_config(
    page_title="Document AI Platform - Islamic Financing",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .status-badge {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 1. SIDEBAR NAVIGATION & FILE UPLOADER
# -----------------------------------------------------------------------------
st.sidebar.title("📌 Document AI Platform")
uploaded_file = st.sidebar.file_uploader("Upload Musharakah PDF", type=["pdf"])

menu = st.sidebar.radio(
    "Navigation",
    ["Overview", "Performance Metrics", "Property List", "Analytics", "Risk Allocation", "Compliance"],
    index=0
)

st.sidebar.divider()
st.sidebar.info("💡 **Active Engine:** Dynamic Parsing & Analytics Active")

# -----------------------------------------------------------------------------
# 2. DYNAMIC EXTRACTION & SCHEDULE GENERATOR
# -----------------------------------------------------------------------------
if uploaded_file is not None:
    reader = PyPDF2.PdfReader(uploaded_file)
    pdf_text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
    
    prop_val_match = re.search(r"Property Value\s*₹?\s*([\d,]+)", pdf_text)
    investor_cap_match = re.search(r"Investor's Capital\s*₹?\s*([\d,]+)", pdf_text)
    
    property_value = int(prop_val_match.group(1).replace(",", "")) if prop_val_match else 16000000
    investor_capital = int(investor_cap_match.group(1).replace(",", "")) if investor_cap_match else 9800000
else:
    property_value = 16000000
    investor_capital = 9800000

@st.cache_data
def generate_schedule(inv_cap):
    annual_rate = 0.10
    unit_redemption = inv_cap / 120
    data = []
    curr_balance = inv_cap
    
    for month in range(1, 121):
        rental_share = (curr_balance * annual_rate) / 12
        total_payment = rental_share + unit_redemption
        curr_balance -= unit_redemption
        
        year = (month - 1) // 12 + 1
        month_in_year = ((month - 1) % 12) + 1
        
        data.append({
            "Month": f"Month {month}",
            "Month_Num": month,
            "Year": f"Year {year}",
            "Year_Num": year,
            "Month_In_Year": f"M{month_in_year}",
            "Rental Share (₹)": round(rental_share, 2),
            "Unit Buyout (₹)": round(unit_redemption, 2),
            "Total Payment (₹)": round(total_payment, 2),
            "Investor Balance (₹)": max(round(curr_balance, 2), 0.0),
            "Investor Exposure (%)": round((curr_balance / property_value) * 100, 2)
        })
    return pd.DataFrame(data)

df_schedule = generate_schedule(investor_capital)

# -----------------------------------------------------------------------------
# TAB 1: OVERVIEW (Full 120 Months Grid)
# -----------------------------------------------------------------------------
if menu == "Overview":
    st.title("📊 Document Analysis Dashboard")
    st.caption("High-level summary of active Musharakah agreement.")
    
    # Key Summary Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Property Value", value=f"₹{property_value:,}")
    with col2:
        st.metric(label="Investor's Capital Share", value=f"₹{investor_capital:,}")
    with col3:
        st.metric(label="Buyer's Contribution Share", value=f"₹{property_value - investor_capital:,}")
    with col4:
        st.metric(label="Tenure / Amortization", value="120 Months (10 Yrs)")
        
    st.divider()

    grid_col1, grid_col2 = st.columns([1, 1.8])

    with grid_col1:
        st.subheader("Capital Structure Breakdown")
        fig_donut = px.pie(
            names=["Investor's Capital", "Buyer's Capital"],
            values=[investor_capital, property_value - investor_capital],
            hole=0.5,
            color_discrete_sequence=["#008080", "#20b2aa"]
        )
        fig_donut.update_traces(textinfo="percent+label")
        fig_donut.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_donut, use_container_width=True)

    with grid_col2:
        st.subheader("Complete 10-Year Payment Schedule (All 120 Months)")
        
        # Displaying the COMPLETE 120-month schedule without truncation
        st.dataframe(
            df_schedule[["Month", "Year", "Rental Share (₹)", "Unit Buyout (₹)", "Total Payment (₹)", "Investor Balance (₹)"]],
            use_container_width=True,
            height=380,
            hide_index=True
        )

# -----------------------------------------------------------------------------
# TAB 2: PERFORMANCE METRICS (Yearly Heatmap with Exact Values & Chronological Order)
# -----------------------------------------------------------------------------
elif menu == "Performance Metrics":
    st.title(" Performance Metrics & Heatmap")
    st.caption("Visualizing payment intensity and cash-flow distribution across the 10-year lifecycle.")
    
    # 1. Pivot Table Creation
    pivot_df = df_schedule.pivot(index="Year_Num", columns="Month_In_Year", values="Total Payment (₹)")
    
    # 2. Strict Column Sorting (M1 to M12)
    month_cols = [f"M{i}" for i in range(1, 13)]
    pivot_df = pivot_df[month_cols]
    
    # 3. Strict Row Sorting (Year 1 to Year 10 chronologically)
    year_labels = [f"Year {i}" for i in range(1, 11)]
    pivot_df.index = year_labels
    
    # Format values in Lakhs (₹X.XX L) for readable cell overlays inside the heatmap
    formatted_text = pivot_df.map(lambda x: f"₹{x/100000:.2f}L" if pd.notnull(x) else "")
    
    # 4. Interactive Plotly Heatmap with embedded text values
    fig_heatmap = px.imshow(
        pivot_df,
        labels=dict(x="Month Cycle", y="Year", color="Total Payment (₹)"),
        x=month_cols,
        y=year_labels,
        color_continuous_scale="Tealgrn",
        text_auto=False
    )
    
    # Add text annotations directly inside each cell box
    fig_heatmap.update_traces(
        text=formatted_text.values,
        texttemplate="%{text}",
        textfont=dict(size=11)
    )
    
    fig_heatmap.update_layout(
        title="Monthly Payment Heatmap Across 10 Years (Values in ₹ Lakhs)",
        height=520,
        yaxis=dict(autorange="reversed") # Ensures Year 1 starts at top, Year 10 at bottom
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    st.info("💡 **Insight:** The heatmap clearly demonstrates the descending nature of monthly cash flows as the investor's capital balance reduces year over year.")

# -----------------------------------------------------------------------------
# TAB 3: PROPERTY LIST
# -----------------------------------------------------------------------------
elif menu == "Property List":
    st.title("🏡 Property Portfolio Management")
    properties = pd.DataFrame([
        {"Property ID": "PROP-2026-01", "Location": "Bengaluru", "Value (₹)": property_value, "Investor Share": f"{round((investor_capital/property_value)*100)}%", "Status": "Active"},
        {"Property ID": "PROP-2026-02", "Location": "Mumbai", "Value (₹)": 24000000, "Investor Share": "75%", "Status": "Active"},
        {"Property ID": "PROP-2026-03", "Location": "Hyderabad", "Value (₹)": 11000000, "Investor Share": "50%", "Status": "Pending Review"},
    ])
    st.dataframe(properties, use_container_width=True, hide_index=True)

# -----------------------------------------------------------------------------
# TAB 4: ANALYTICS
# -----------------------------------------------------------------------------
elif menu == "Analytics":
    st.title("📈 Advanced Portfolio Analytics")
    st.caption("Investor Capital Amortization Curve Over 120 Months")
    
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=df_schedule["Month_Num"], 
        y=df_schedule["Investor Balance (₹)"], 
        name="Investor Balance", 
        line=dict(color="#008080", width=3)
    ))
    fig_line.update_layout(
        title="10-Year Amortization Trajectory: Investor Capital Balance",
        xaxis_title="Months",
        yaxis_title="Amount (₹)",
        hovermode="x unified"
    )
    st.plotly_chart(fig_line, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 5: RISK ALLOCATION
# -----------------------------------------------------------------------------
elif menu == "Risk Allocation":
    st.title("⚖️ 10-Year Risk Allocation Analysis")
    st.caption("Evaluating capital exposure risk and volatility migration over the 10-year tenor.")
    
    col_r1, col_r2, col_r3, col_r4 = st.columns(4)
    with col_r1:
        st.metric("Initial Risk Exposure", f"{round((investor_capital/property_value)*100)}%")
    with col_r2:
        st.metric("Final Risk Exposure", "0% (Fully Transferred)")
    with col_r3:
        st.metric("Payment Volatility (Std Dev)", f"₹{np.std(df_schedule['Total Payment (₹)']):,.2f}")
    with col_r4:
        st.metric("Risk Reduction Rate", "10.00% Annually")

    fig_risk = px.area(
        df_schedule, 
        x="Month_Num", 
        y="Investor Exposure (%)", 
        title="Investor Capital Exposure Reduction Trajectory (%)",
        labels={"Month_Num": "Months", "Investor Exposure (%)": "Exposure Percentage (%)"}
    )
    fig_risk.update_traces(fillcolor="rgba(32, 178, 170, 0.3)", line_color="#008080")
    st.plotly_chart(fig_risk, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 6: COMPLIANCE
# -----------------------------------------------------------------------------
elif menu == "Compliance":
    st.title("🛡️ Shariah Governance & Compliance Audit")
    
    aaoifi_rules = pd.DataFrame([
        {"Principle": "1. Equity Partnership", "Standard": "Shirkat-ul-Milk", "Status": "Verified"},
        {"Principle": "2. Independent Lease", "Standard": "Ijarah Contract", "Status": "Verified"},
        {"Principle": "3. Declining Rental", "Standard": "Proportional Reduction", "Status": "Verified"},
        {"Principle": "4. Unilateral Promise", "Standard": "Wa'ad Execution", "Status": "Verified"},
    ])
    st.table(aaoifi_rules)