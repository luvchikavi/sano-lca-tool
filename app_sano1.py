import pandas as pd
import streamlit as st
import plotly.express as px

# Hardcoded dataset (from CSV)
data_dict = [
    {"Product Name": "Sano Maxima Laundry Detergent", "Raw Material (kg CO2)": 50, "Production (kg CO2)": 30.0, "Logistics (kg CO2)": 20, "Total Carbon Footprint (kg CO2)": 100.0},
    {"Product Name": "Sano Floor Cleaner", "Raw Material (kg CO2)": 52, "Production (kg CO2)": 31.5, "Logistics (kg CO2)": 21, "Total Carbon Footprint (kg CO2)": 104.5},
    {"Product Name": "Sano Dishwasher Tablets", "Raw Material (kg CO2)": 54, "Production (kg CO2)": 33.0, "Logistics (kg CO2)": 22, "Total Carbon Footprint (kg CO2)": 109.0},
    {"Product Name": "Sano Anti-Lime Scale", "Raw Material (kg CO2)": 56, "Production (kg CO2)": 34.5, "Logistics (kg CO2)": 23, "Total Carbon Footprint (kg CO2)": 113.5},
    {"Product Name": "Sano Toilet Cleaner", "Raw Material (kg CO2)": 58, "Production (kg CO2)": 36.0, "Logistics (kg CO2)": 24, "Total Carbon Footprint (kg CO2)": 118.0}
]

# Convert dictionary to pandas DataFrame
data = pd.DataFrame(data_dict)

# Dashboard Configuration
st.set_page_config(page_title="Sano LCA Dashboard", layout="wide")

# Display Sano Logo and Title
col_logo, col_title = st.columns([1, 3])
with col_logo:
    st.image("image.png", width=150)  # Ensure the logo is in the same directory
with col_title:
    st.title("Sano LCA Dashboard - Demo")

# Sidebar Navigation
st.sidebar.header("Navigation")
selected_tab = st.sidebar.radio("Select a tab:", ["Environmental Analysis", "Financial Analysis", "Regulatory Compliance"])

# Define filtered data globally
filtered_data = data.copy()

# Environmental Analysis Tab
if selected_tab == "Environmental Analysis":
    st.sidebar.header("Adjust Parameters")
    transport_type = st.sidebar.selectbox("Transportation Type", ["Air", "Road", "Sea"], key="transport")
    energy_source = st.sidebar.selectbox("Energy Source", ["Renewable", "Non-renewable"], key="energy")
    export_ratio = st.sidebar.slider("Percent of Products Exported to EU", 0, 100, 20, key="export")

    # Filter data based on sidebar inputs
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

# Financial Analysis Tab
elif selected_tab == "Financial Analysis":
    st.header("Financial Analysis")
    carbon_price = 25.0
    st.metric(label="Current Carbon Credit Price (€/ton)", value=f"€{carbon_price}")

    # Financial Projections
    carbon_emissions = filtered_data["Total Carbon Footprint (kg CO2)"].sum() / 1000  # Convert to tons
    total_cost = carbon_emissions * carbon_price
    st.write(f"### Total Carbon Emissions: {carbon_emissions:.2f} tons")
    st.write(f"### Estimated Carbon Costs: €{total_cost:.2f}")

# Regulatory Compliance Tab
elif selected_tab == "Regulatory Compliance":
    st.header("Regulatory Compliance Tools")
    st.write("Upload compliance datasets for analysis.")

# Footer
st.write("---")
st.write("**Note:** This is a demo dashboard for illustrating LCA tracking, CBAM compliance, and financial impact analysis.")
