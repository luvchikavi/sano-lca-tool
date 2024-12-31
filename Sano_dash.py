import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "sano_lca_products.csv")
LOGO_FILE = os.path.join(BASE_DIR, "image.png")

# Check if files exist
if not os.path.exists(DATA_FILE):
    st.error(f"Missing required data file: {DATA_FILE}. Please upload this file to the repository.")
    st.stop()

if not os.path.exists(LOGO_FILE):
    st.error(f"Missing required logo file: {LOGO_FILE}. Please upload this file to the repository.")
    st.stop()

# Load data
try:
    data = pd.read_csv(DATA_FILE)
    st.write("### Loaded Data")
    st.write(data.head())  # Display the first few rows to ensure data is loaded correctly

    # Ensure columns are as expected
    expected_columns = [
        "Product Name",
        "Raw Material (kg CO2)",
        "Production (kg CO2)",
        "Logistics (kg CO2)",
        "Total Carbon Footprint (kg CO2)"
    ]
    if not all(column in data.columns for column in expected_columns):
        st.error(f"The dataset does not contain the expected columns: {expected_columns}")
        st.write("Found columns:", list(data.columns))
        st.stop()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Dashboard Configuration
st.set_page_config(page_title="Sano LCA Dashboard", layout="wide")

# Display Sano Logo and Title
col_logo, col_title = st.columns([1, 3])
with col_logo:
    st.image(LOGO_FILE, width=150)
with col_title:
    st.title("Sano LCA Dashboard - Demo")

# Sidebar Navigation
st.sidebar.header("Navigation")
selected_tab = st.sidebar.radio("Select a tab:", ["Environmental Analysis", "Financial Analysis", "Regulatory Compliance"])

if selected_tab == "Environmental Analysis":
    st.header("Environmental Analysis")

    # Display data
    st.subheader("Product Data")
    st.dataframe(data, height=400)

    # Visualize emissions by product
    st.subheader("Emissions Breakdown")
    pie_chart = px.pie(
        data,
        values="Total Carbon Footprint (kg CO2)",
        names="Product Name",
        title="Emissions by Product",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(pie_chart)

elif selected_tab == "Financial Analysis":
    st.header("Financial Analysis")

    # Example static calculation
    carbon_price = 25  # €/ton, example price
    total_emissions = data["Total Carbon Footprint (kg CO2)"].sum() / 1000  # Convert to tons
    total_cost = total_emissions * carbon_price

    st.write(f"### Total Emissions: {total_emissions:.2f} tons")
    st.write(f"### Estimated Carbon Cost: €{total_cost:.2f}")

elif selected_tab == "Regulatory Compliance":
    st.header("Regulatory Compliance")

    st.subheader("Upload Compliance Data")
    uploaded_file = st.file_uploader("Upload a CSV file for compliance rules", type="csv")

    if uploaded_file is not None:
        compliance_data = pd.read_csv(uploaded_file)
        st.write("### Uploaded Compliance Rules")
        st.dataframe(compliance_data)
    else:
        st.write("No compliance data uploaded.")

# Footer
st.write("---")
st.write("**Note:** This dashboard is a demo version. Ensure all required files are uploaded for full functionality.")
