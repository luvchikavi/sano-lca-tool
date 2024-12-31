import streamlit as st
import pandas as pd
import plotly.express as px
<<<<<<< HEAD
import requests

# Load default product data
default_data_path = '/Users/aviluvchik/Python Projects/Sano/sano_lca_products.csv'  # Ensure the file is in the correct directory
data = pd.read_csv(default_data_path)
=======

# Embed the default dataset
DEFAULT_DATA = {
    "Product Name": ["Product A", "Product B", "Product C"],
    "Raw Material (kg CO2)": [50, 70, 30],
    "Production (kg CO2)": [100, 150, 120],
    "Logistics (kg CO2)": [20, 25, 15],
    "Total Carbon Footprint (kg CO2)": [170, 245, 165]
}

def load_default_data():
    return pd.DataFrame(DEFAULT_DATA)
>>>>>>> 32b4e24 (Initial commit with Streamlit dashboard)

# Dashboard Configuration
st.set_page_config(page_title="Sano LCA Dashboard", layout="wide")

# Display Sano Logo and Title
<<<<<<< HEAD
col_logo, col_title = st.columns([1, 3])
with col_logo:
    logo_path = '/Users/aviluvchik/Python Projects/Sano/image.png'  # Ensure the logo file is in the correct directory
    st.image(logo_path, width=150)
with col_title:
    st.title("Sano LCA Dashboard - Demo")
=======
st.title("Sano LCA Dashboard - Demo")
st.write("This dashboard analyzes carbon footprints for products and compliance.")
>>>>>>> 32b4e24 (Initial commit with Streamlit dashboard)

# Sidebar Navigation
st.sidebar.header("Navigation")
selected_tab = st.sidebar.radio("Select a tab:", ["Environmental Analysis", "Financial Analysis", "Regulatory Compliance"])

<<<<<<< HEAD
# Define filtered_data globally
filtered_data = data.copy()

if selected_tab == "Environmental Analysis":
    # Sidebar for Parameters
    st.sidebar.header("Adjust Parameters")
    transport_type = st.sidebar.selectbox("Transportation Type", ["Air", "Road", "Sea"], key="transport")
    energy_source = st.sidebar.selectbox("Energy Source", ["Renewable", "Non-renewable"], key="energy")
    export_ratio = st.sidebar.slider("Percent of Products Exported to EU", 0, 100, 20, key="export")

    # Filter Data Based on Sidebar Inputs
    if transport_type == "Air":
        filtered_data["Logistics (kg CO2)"] *= 1.5
    elif transport_type == "Sea":
        filtered_data["Logistics (kg CO2)"] *= 0.8

    if energy_source == "Renewable":
        filtered_data["Production (kg CO2)"] *= 0.7
    else:
        filtered_data["Production (kg CO2)"] *= 1.2

    # Update Total Carbon Footprint
    filtered_data["Total Carbon Footprint (kg CO2)"] = (
        filtered_data["Raw Material (kg CO2)"] +
        filtered_data["Production (kg CO2)"] +
        filtered_data["Logistics (kg CO2)"]
    )

    # Main Layout
    st.header("Product List and Carbon Footprints")
    col1, col2 = st.columns(2)

    # Product Table
    with col1:
        st.subheader("Product List")
        st.dataframe(filtered_data, height=400)

    # Emissions Breakdown Pie Chart
    with col2:
        st.subheader("Emissions Breakdown for All Products")
        pie_chart = px.pie(
            filtered_data,
            values="Total Carbon Footprint (kg CO2)",
            names="Product Name",
            title="Total Emissions by Product",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(pie_chart)

    # Interactive Product Analysis
    st.header("Product Analysis")
    col_left, col_right = st.columns([2, 1])
    with col_left:
        selected_product = st.selectbox("Select a Product to View Details", filtered_data["Product Name"], key="product")
        product_data = filtered_data[filtered_data["Product Name"] == selected_product]
        st.write(f"### Details for {selected_product}")
        st.write(product_data)
    with col_right:
        product_pie = px.pie(
            product_data.melt(id_vars=["Product Name"], value_vars=[
                "Raw Material (kg CO2)", "Production (kg CO2)", "Logistics (kg CO2)"
            ]),
            values="value",
            names="variable",
            title=f"Emissions Breakdown for {selected_product}",
            color_discrete_sequence=px.colors.sequential.Blues
        )
        st.plotly_chart(product_pie)

    # Additional Interactivity: Filter by Carbon Footprint Range
    st.sidebar.header("Additional Filters")
    min_footprint, max_footprint = st.sidebar.slider(
        "Filter by Total Carbon Footprint (kg CO2)",
        int(filtered_data["Total Carbon Footprint (kg CO2)"].min()),
        int(filtered_data["Total Carbon Footprint (kg CO2)"].max()),
        (int(filtered_data["Total Carbon Footprint (kg CO2)"].min()), int(filtered_data["Total Carbon Footprint (kg CO2)"].max()))
    )

    filtered_data = filtered_data[
        (filtered_data["Total Carbon Footprint (kg CO2)"] >= min_footprint) &
        (filtered_data["Total Carbon Footprint (kg CO2)"] <= max_footprint)
    ]
=======
# File Upload
st.sidebar.header("Upload Your Data")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type="csv")

# Load data based on file upload or default
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.sidebar.success("Data uploaded successfully!")
else:
    st.sidebar.warning("Using default dataset.")
    data = load_default_data()

if selected_tab == "Environmental Analysis":
    st.header("Environmental Analysis")

    # Display Product Data
    st.subheader("Product List and Carbon Footprints")
    st.dataframe(data)

    # Emissions Breakdown Pie Chart
    st.subheader("Emissions Breakdown")
    pie_chart = px.pie(
        data,
        values="Total Carbon Footprint (kg CO2)",
        names="Product Name",
        title="Emissions by Product",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(pie_chart)
>>>>>>> 32b4e24 (Initial commit with Streamlit dashboard)

elif selected_tab == "Financial Analysis":
    st.header("Financial Analysis")

<<<<<<< HEAD
    # Carbon Credit Price API Example (replace with actual API if available)
    st.subheader("Live Carbon Credit Prices")
    try:
        # Simulated API call
        carbon_price_response = {"price": 25.0}  # Replace with actual API call if available
        carbon_price = carbon_price_response["price"]
        st.metric(label="Current Carbon Credit Price (€/ton)", value=f"€{carbon_price}")
    except Exception as e:
        st.error("Unable to fetch live carbon credit prices.")

    # Financial Projections Example
    st.subheader("Cost Projections")
    filtered_data["Total Carbon Footprint (kg CO2)"] = (
        filtered_data["Raw Material (kg CO2)"] +
        filtered_data["Production (kg CO2)"] +
        filtered_data["Logistics (kg CO2)"]
    )
    carbon_emissions = filtered_data["Total Carbon Footprint (kg CO2)"].sum() / 1000  # Convert to tons
    total_cost = carbon_emissions * carbon_price
    st.write(f"### Total Carbon Emissions: {carbon_emissions:.2f} tons")
    st.write(f"### Estimated Carbon Costs: €{total_cost:.2f}")

    # Carbon Tax Analysis
    st.subheader("Carbon Tax Analysis")
    carbon_tax_rate = st.slider("Carbon Tax Rate (€/ton)", min_value=10, max_value=100, value=50, step=5)
    total_tax_cost = carbon_emissions * carbon_tax_rate
    st.write(f"### Carbon Tax Rate: €{carbon_tax_rate} per ton")
    st.write(f"### Estimated Carbon Tax Costs: €{total_tax_cost:.2f}")

    # Visualize Cost Distribution
    cost_chart = px.bar(
        filtered_data,
        x="Product Name",
        y="Total Carbon Footprint (kg CO2)",
        title="Cost Distribution by Product",
        labels={"Total Carbon Footprint (kg CO2)": "Carbon Footprint (kg CO2)"},
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(cost_chart)

    # Automated Updates Example
    st.subheader("Automated Financial Updates")
    st.write("Future integration with APIs to fetch live energy costs and taxation updates.")

elif selected_tab == "Regulatory Compliance":
    st.header("Regulatory Compliance Tools")

    # Upload Dataset Section for Custom Compliance Data
    st.subheader("Upload Compliance Rules or Data")
    uploaded_compliance_file = st.file_uploader("Upload a CSV file with regulatory rules or data", type="csv")

    if uploaded_compliance_file is not None:
        compliance_data = pd.read_csv(uploaded_compliance_file)
        st.write("### Uploaded Compliance Data")
        st.dataframe(compliance_data)

        # Compliance Analysis
        st.subheader("Compliance Analysis")
        def check_compliance(row, compliance_data):
            threshold = compliance_data["Threshold"].iloc[0]
            return "Compliant" if row["Total Carbon Footprint (kg CO2)"] <= threshold else "Non-Compliant"

        filtered_data["Compliance Status"] = filtered_data.apply(
            lambda row: check_compliance(row, compliance_data), axis=1
        )

        st.write("### Compliance Results")
        st.dataframe(filtered_data[["Product Name", "Total Carbon Footprint (kg CO2)", "Compliance Status"]])

        compliance_summary = filtered_data["Compliance Status"].value_counts()
        compliance_chart = px.pie(
            compliance_summary,
            values=compliance_summary.values,
            names=compliance_summary.index,
            title="Compliance Status Overview",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(compliance_chart)
    else:
        st.write("No compliance data uploaded yet.")
=======
    # Carbon Credit Cost Calculation
    st.subheader("Carbon Credit Cost Calculation")
    carbon_price = st.slider("Set Carbon Credit Price (€/ton)", min_value=10, max_value=100, value=25, step=5)
    total_emissions = data["Total Carbon Footprint (kg CO2)"].sum() / 1000  # Convert to tons
    total_cost = total_emissions * carbon_price

    st.write(f"### Total Carbon Emissions: {total_emissions:.2f} tons")
    st.write(f"### Estimated Carbon Credit Cost: €{total_cost:.2f}")

elif selected_tab == "Regulatory Compliance":
    st.header("Regulatory Compliance")

    # Compliance Analysis (Example)
    st.subheader("Compliance Status")
    compliance_threshold = st.slider("Set Compliance Threshold (kg CO2)", min_value=100, max_value=300, value=200, step=10)

    data["Compliance Status"] = data["Total Carbon Footprint (kg CO2)"].apply(
        lambda x: "Compliant" if x <= compliance_threshold else "Non-Compliant"
    )

    st.write("### Compliance Results")
    st.dataframe(data[["Product Name", "Total Carbon Footprint (kg CO2)", "Compliance Status"]])

    compliance_summary = data["Compliance Status"].value_counts()
    compliance_chart = px.pie(
        compliance_summary,
        values=compliance_summary.values,
        names=compliance_summary.index,
        title="Compliance Status Overview",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(compliance_chart)
>>>>>>> 32b4e24 (Initial commit with Streamlit dashboard)

# Footer
st.write("---")
st.write("**Note:** This is a demo dashboard for illustrating LCA tracking, CBAM compliance, and financial impact analysis.")
