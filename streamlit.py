import streamlit as st
import plotly.express as px
import pandas as pd
import requests
import json

st.set_page_config(layout="wide")

# Custom CSS to change background color to dark grey and increase the width
st.markdown(
    """
    <style>
    .stApp {
        background-color: #2f2f2f;
        color: #ffffff;
        max-width: 2000px;
        margin: auto;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    .reportColumn {
        width: 60% !important;
    }
    .chartColumn {
        width: 40% !important;
    }
    .data-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 12px;
        margin-top: 10px;
        margin-bottom: 30px;
    }
    .data-table th, .data-table td {
        border: 1px solid #ddd;
        padding: 4px;
        text-align: center;
    }
    .data-table th {
        background-color: #1f1f1f;
        color: white;
    }
    .data-table td {
        color: black;
        background-color: white;
    }
    .reportText {
        word-wrap: break-word;
        white-space: normal;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Country selection dropdown
selected_country = st.selectbox('Select a Country:', ['Israel', 'Mexico', 'Qatar', 'Saudi Arabia'])

# Define the URL for the process_json endpoint
url = "https://my-combined-app-vpljqiia2a-uc.a.run.app/process_json"

# Function to fetch data with pagination
def fetch_data(payload, page=1):
    payload["sample_key"] = payload["sample_key"].replace('"page": 1', f'"page": {page}')
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to retrieve data from the process_json endpoint for page {page}")
        return []

# Update the payload dynamically based on selected country
payload = {
    "sample_key": f'{{"db_path": "credit_research.db", "table": "FullReport", "filters": {{"Country": "{selected_country}"}}, "fields": "*", "page": 1, "page_size": 10}}'
}

# Fetch data for pages 1 and 2
all_data = []
for page in range(1, 3):  # Fetching page 1 and 2
    data_chunk = fetch_data(payload, page)
    if data_chunk:
        all_data.extend(data_chunk)

# If data is available, use the first chunk for display
if all_data:
    report = all_data[0]
else:
    st.error("No data available to display")
    st.stop()

# Layout: Two columns, left for the report, right for the charts
col1, col2 = st.columns([6, 4])

# Generate the report in the left-hand column
with col1:
    st.markdown('<div class="reportColumn">', unsafe_allow_html=True)
    st.markdown(f'<h1 class="reportText">{report.get("Title", "Credit Research Report")}</h1>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="reportText">Country Information</h2>', unsafe_allow_html=True)
    st.markdown(f'<p class="reportText">Country: {report.get("Country", "N/A")}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="reportText">Ownership: {report.get("Ownership", "N/A")}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="reportText">NFA Rating: {report.get("NFARating", "N/A")}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="reportText">ESG Rating: {report.get("ESGRating", "N/A")}</p>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="reportText">Overview</h2>', unsafe_allow_html=True)
    st.markdown(f'<p class="reportText">{report.get("Overview", "No overview available.")}</p>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="reportText">Politics</h2>', unsafe_allow_html=True)
    st.markdown(f'<p class="reportText">{report.get("PoliticalNews", "No political news available.")}</p>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="reportText">Strengths</h2>', unsafe_allow_html=True)
    st.markdown(f'<p class="reportText">{report.get("Strengths", "No strengths information available.")}</p>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="reportText">Weaknesses</h2>', unsafe_allow_html=True)
    st.markdown(f'<p class="reportText">{report.get("Weaknesses", "No weaknesses information available.")}</p>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="reportText">Opportunities</h2>', unsafe_allow_html=True)
    st.markdown(f'<p class="reportText">{report.get("Opportunities", "No opportunities information available.")}</p>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="reportText">Threats</h2>', unsafe_allow_html=True)
    st.markdown(f'<p class="reportText">{report.get("Threats", "No threats information available.")}</p>', unsafe_allow_html=True)

    st.markdown('<h2 class="reportText">Recent News</h2>', unsafe_allow_html=True)
    st.markdown(f'<p class="reportText">{report.get("RecentNews", "No recent news available.")}</p>', unsafe_allow_html=True)

    st.markdown('<h2 class="reportText">Ratings and Comments from Credit Rating Agencies</h2>', unsafe_allow_html=True)
    st.markdown('<h3 class="reportText">Moody\'s:</h3>', unsafe_allow_html=True)
    st.markdown(f'<p class="reportText">{report.get("MoodysRating", "N/A")}</p>', unsafe_allow_html=True)
    
    st.markdown('<h3 class="reportText">S&P Global Ratings:</h3>', unsafe_allow_html=True)
    st.markdown(f'<p class="reportText">{report.get("SPGlobalRating", "N/A")}</p>', unsafe_allow_html=True)
    
    st.markdown('<h3 class="reportText">Fitch Ratings:</h3>', unsafe_allow_html=True)
    st.markdown(f'<p class="reportText">{report.get("FitchRating", "N/A")}</p>', unsafe_allow_html=True)

    st.markdown('<h2 class="reportText">Conclusion</h2>', unsafe_allow_html=True)
    st.markdown(f'<p class="reportText">{report.get("Conclusion", "No conclusion available.")}</p>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Generate the charts and data tables in the right-hand column
with col2:
    st.markdown('<div class="chartColumn">', unsafe_allow_html=True)
    st.header("Economic Data (2024 Onwards)")

    # Define the custom color palette
    color_palette = ["#FFA500", "#007FFF", "#DC143C", "#32CD32", "#FFD700", "#4B0082"]

    def plot_chart(df, y_column, title):
        fig = px.bar(df, x='Year', y=y_column,
                     title=title,
                     color_discrete_sequence=color_palette,
                     height=300)
        fig.update_traces(marker_line_width=0)
        fig.update_layout(
            plot_bgcolor='#2f2f2f',
            paper_bgcolor='#2f2f2f',
            font=dict(color='white'),
            autosize=True
        )
        return fig

    def create_data_table(df, y_column):
        table_html = "<table class='data-table'>"
        table_html += "<tr><th>Year</th>" + "".join([f"<th>{year}</th>" for year in df['Year']]) + "</tr>"
        table_html += f"<tr><td>{y_column}</td>"
        for value in df[y_column]:
            table_html += f"<td>{value:.2f}</td>"
        table_html += "</tr></table>"
        return table_html

    # Create all dataframes
    charts_data = [
        ("GDP Growth (%)", [report.get(f'GDPGrowthRateYear{i}', 0) for i in range(1, 7)]),
        ("Inflation Rate (%)", [report.get(f'InflationYear{i}', 0) for i in range(1, 7)]),
        ("Unemployment Rate (%)", [report.get(f'UnemploymentRateYear{i}', 0) for i in range(1, 7)]),
        ("Population (millions)", [report.get(f'PopulationYear{i}', 0) for i in range(1, 7)]),
        ("Government Budget Balance (% of GDP)", [report.get(f'GovernmentFinancesYear{i}', 0) for i in range(1, 7)]),
        ("Current Account Balance (% of GDP)", [report.get(f'CurrentAccountBalanceYear{i}', 0) for i in range(1, 7)])
    ]

    years = [2024, 2025, 2026, 2027, 2028, 2029]

    for metric, values in charts_data:
        df = pd.DataFrame({
            "Year": years,
            metric: values
        })

        # Display the chart
        st.plotly_chart(plot_chart(df, metric, metric), use_container_width=True)

        # Display the data table
        st.markdown(create_data_table(df, metric), unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


