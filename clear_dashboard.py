import os
import pandas as pd
import streamlit as st
import plotly.express as px
import requests  # To interact with the CBAM audit system

# Automatically change the working directory to the script's directory
os.chdir(os.path.dirname(__file__))

# Set page configuration
st.set_page_config(page_title="CLEAR Dashboard", layout="wide")

# Initial Landing Page
if "start" not in st.session_state:
    st.session_state.start = False

if not st.session_state.start:
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        st.image("CLEAR_LOGO.png", width=100)
    with col_title:
        st.title("Welcome to the CLEAR Dashboard")

    st.markdown(
        """
        ### About CLEAR
        CLEAR (Compliance, Lifecycle Emissions Analysis, and Reporting) is a cutting-edge decision-making tool designed
        to help industries streamline their sustainability and compliance strategies.
        
        It provides an integrated platform for:
        - **Analyzing environmental impacts**
        - **Estimating financial costs**, including carbon taxes
        - **Ensuring regulatory compliance** with frameworks like CBAM, REACH, and more.
        - **Model Simultaion** for better decision making and reliable results. 

        By connecting to the most up-to-date Life Cycle Assessment (LCA) and regulatory databases, CLEAR ensures users always
        work with the latest and most accurate information.

        ### About Dr. Avi Luvchik
        Avi  is an internationally recognized expert in sustainability and environmental compliance. With over 
        20 years of experience, he has advised top organizations across various industries. His expertise spans life cycle 
        assessments, emissions reduction, and corporate sustainability strategies. Dr. Luvchik is the founder of CLEAR and 
        continues to innovate solutions to tackle global environmental challenges.
        """
    )

    # Footer and Button Section
    st.write("---")
    if st.button("Let's Get Started"):
        st.session_state.start = True

    st.markdown(
        """
        **CLEAR v1.0**  
        Tool developed by Dr. Avi Luvchik  
        @ All rights reserved
        """,
        unsafe_allow_html=True
    )
    st.stop()

# Load dataset
@st.cache_data
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        return pd.DataFrame()

@st.cache_data
def process_uploaded_data(uploaded_file):
    try:
        return pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return pd.DataFrame()

# Sidebar Data Upload
st.sidebar.header("Data Management")
data_file = st.sidebar.file_uploader("Upload a CSV File", type=["csv"])
if data_file:
    data = process_uploaded_data(data_file)
else:
    data = load_data("sano_lca_products.csv")

if data.empty:
    st.error("Dataset could not be loaded. Please ensure the CSV file is available.")
    st.stop()

# Header Section
col_logo, col_title = st.columns([1, 4])
with col_logo:
    try:
        st.image("client_logo.png", width=140)  # Display client logo
    except FileNotFoundError:
        st.warning("Client logo not found. Please upload a valid logo file.")
with col_title:
    pass  # Remove the CLEAR title after starting the application

# Sidebar Navigation
st.sidebar.header("Navigation")
selected_tab = st.sidebar.radio("Select a tab:", ["Environmental Analysis", "Financial Analysis", "Regulatory Compliance", "Audit Progress"])

# Environmental Analysis Tab
if selected_tab == "Environmental Analysis":
    st.header("🌿 Environmental Analysis")

    # Scenario Modeling Sliders
    st.sidebar.header("Adjust Parameters")
    transport_type = st.sidebar.selectbox("Transportation Type", ["Air", "Road", "Sea"], key="transport")
    energy_source = st.sidebar.selectbox("Energy Source", ["Renewable", "Non-renewable"], key="energy")
    export_ratio = st.sidebar.slider("Percent of Products Exported to EU", 0, 100, 20, key="export")

    # Adjust emissions based on scenario inputs
    adjusted_data = data.copy()
    if transport_type == "Air":
        adjusted_data["Logistics (kg CO2)"] *= 1.5
    elif transport_type == "Sea":
        adjusted_data["Logistics (kg CO2)"] *= 0.8

    if energy_source == "Renewable":
        adjusted_data["Production (kg CO2)"] *= 0.7
    else:
        adjusted_data["Production (kg CO2)"] *= 1.2

    # Update Total Carbon Footprint
    adjusted_data["Total Carbon Footprint (kg CO2)"] = (
        adjusted_data["Raw Material (kg CO2)"] +
        adjusted_data["Production (kg CO2)"] +
        adjusted_data["Logistics (kg CO2)"]
    )

    # Display Adjusted Metrics
    st.subheader("Adjusted Emissions Data")
    st.dataframe(adjusted_data[["Product Name", "Raw Material (kg CO2)", "Production (kg CO2)", "Logistics (kg CO2)", "Total Carbon Footprint (kg CO2)"]])

    # Emissions Breakdown Pie Chart
    st.subheader("Emissions Breakdown by Category")
    pie_chart = px.pie(
        adjusted_data.melt(id_vars="Product Name", value_vars=["Raw Material (kg CO2)", "Production (kg CO2)", "Logistics (kg CO2)"], var_name="Category", value_name="Emissions (kg CO2)"),
        values="Emissions (kg CO2)",
        names="Category",
        title="Emissions Distribution",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(pie_chart, use_container_width=True)

    # Bar Chart for Per-Product Emissions
    st.subheader("Per-Product Emissions Comparison")
    bar_chart = px.bar(
        adjusted_data,
        x="Product Name",
        y="Total Carbon Footprint (kg CO2)",
        title="Total Emissions by Product",
        labels={"Product Name": "Product", "Total Carbon Footprint (kg CO2)": "Total Emissions (kg CO2)"},
        color="Total Carbon Footprint (kg CO2)",
        color_continuous_scale=px.colors.sequential.Blues
    )
    st.plotly_chart(bar_chart, use_container_width=True)

# Financial Analysis Tab
elif selected_tab == "Financial Analysis":
    st.header("💰 Financial Analysis")

    # Carbon Tax Slider
    carbon_tax_rate = st.slider("Set Carbon Tax Rate (€/ton)", min_value=10, max_value=100, value=25, step=5)

    # Calculate Total Carbon Emissions (tons)
    data["Total Carbon Footprint (tons)"] = data["Total Carbon Footprint (kg CO2)"] / 1000
    data["Carbon Tax (€)"] = data["Total Carbon Footprint (tons)"] * carbon_tax_rate

    # Display Metrics
    total_emissions = data["Total Carbon Footprint (tons)"].sum()
    total_tax_cost = data["Carbon Tax (€)"].sum()

    st.metric(label="Total Carbon Emissions (tons)", value=f"{total_emissions:.2f}")
    st.metric(label="Total Carbon Tax Cost (€)", value=f"€{total_tax_cost:.2f}")

    # Cost Breakdown Table
    st.subheader("Cost Breakdown by Product")
    st.dataframe(data[["Product Name", "Total Carbon Footprint (tons)", "Carbon Tax (€)"]])

    # Bar Chart for Cost Distribution
    st.subheader("Cost Distribution by Product")
    bar_chart = px.bar(
        data,
        x="Product Name",
        y="Carbon Tax (€)",
        title="Carbon Tax Costs by Product",
        labels={"Product Name": "Product", "Carbon Tax (€)": "Tax Cost (€)"},
        color="Carbon Tax (€)",
        color_continuous_scale=px.colors.sequential.Blues
    )
    st.plotly_chart(bar_chart, use_container_width=True)

# Regulatory Compliance Tab
elif selected_tab == "Regulatory Compliance":
    st.header("📜 Regulatory Compliance Tools")

    # Regulatory Summary Table
    st.subheader("Relevant Regulations for the Chemical Sector")
    regulations = pd.DataFrame({
        "Regulation Name": [
            "CBAM (Carbon Border Adjustment Mechanism)",
            "TSCA (Toxic Substances Control Act)",
            "REACH (Registration, Evaluation, Authorization, and Restriction of Chemicals)",
            "GHS (Globally Harmonized System)",
            "EPA Clean Air Act"
        ],
        "Region": ["European Union", "United States", "European Union", "International", "United States"],
        "Exposure Level (1-10)": [10, 7, 9, 6, 5],
        "Description": [
            "Imposes a carbon tax on imported goods based on their embedded emissions.",
            "Regulates the introduction and use of new or existing chemicals.",
            "Ensures high levels of health and environmental protection by tracking chemicals.",
            "Standardizes classification and labeling of chemicals globally.",
            "Limits emissions of hazardous air pollutants."
        ]
    })
    st.dataframe(regulations)

    # Bar Chart for Exposure Levels
    st.subheader("Exposure Levels by Regulation")
    exposure_chart = px.bar(
        regulations,
        x="Regulation Name",
        y="Exposure Level (1-10)",
        title="Regulatory Exposure Levels",
        labels={"Regulation Name": "Regulation", "Exposure Level (1-10)": "Exposure Level"},
        color="Exposure Level (1-10)",
        color_continuous_scale=px.colors.sequential.Emrld
    )
    st.plotly_chart(exposure_chart, use_container_width=True)

# Audit Progress Tab
elif selected_tab == "Audit Progress":
    st.header("🔍 Audit Progress")

    # Fetch data from the CBAM audit system
    try:
        response = requests.get("http://127.0.0.1:5001/compliance_dashboard")
        if response.status_code == 200:
            dashboard_data = response.json()["dashboard"]
            st.metric(label="Total Submissions", value=dashboard_data["total_submissions"])
            st.metric(label="Approved Submissions", value=dashboard_data["approved"])
            st.metric(label="Pending Submissions", value=dashboard_data["pending"])
        else:
            st.error("Failed to fetch audit progress data.")
    except Exception as e:
        st.error(f"Error connecting to the audit system: {e}")

# Footer Attribution
st.write("---")
st.write("**CLEAR v1.0**")
st.write("The CLEAR created by Dr. Avi Luvchik @ All rights reserved.")
