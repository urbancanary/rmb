import streamlit as st
import plotly.express as px
import pandas as pd
import requests
import json

st.set_page_config(layout="wide")

# Custom CSS to change background color to dark grey, adjust column widths, and add margin
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
    margin-right: 8rem;  /* Significantly increase the margin */
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

# Function to fetch data with pagination and error handling
def fetch_data(payload, page=1):
    payload["sample_key"] = payload["sample_key"].replace('"page": 1', f'"page": {page}')
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data for page {page}: {e}")
        st.stop()  # Stop execution if data fetching fails

# Update the payload dynamically based on selected country
payload = {
    "sample_key": f'{{"db_path": "credit_research.db", "table": "FullReport", "filters": {{"Country": "{selected_country}"}}, "fields": "*", "page": 1, "page_size": 10}}'
}

# Fetch data for pages 1 and 2 with error handling
all_data = []
for page in range(1, 3):
    data_chunk = fetch_data(payload, page)
    all_data.extend(data_chunk)

# Check if the first page has data before assigning 'report'
if all_data and len(all_data[0]) > 0:
    report = all_data[0]
else:
    st.error("No data available for the selected country.")
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

# Generate charts and data tables in the right-hand column
with col2:
    st.markdown('<div class="chartColumn">', unsafe_allow_html=True)
    st.header("Economic Data (2024 Onwards)")

    # Updated custom color palette for dark grey background
    color_palette = [
        "#FFA500",  # Bright Orange
        "#007FFF",  # Azure Blue
        "#DC143C",  # Cherry Red
        "#39FF14",  # Electric Lime Green
        "#00FFFF",  # Cyan
        "#DA70D6"   # Vivid Purple
    ]

    def plot_chart(df, y_column, title, color):
        # Determine the min and max for the y-axis
        y_min = df[y_column].min()
        y_max = df[y_column].max()

        # Adjust the y-axis range based on the data:
        if y_min >= 0:  # Positive values only
            y_range = [y_min - 0.05 * (y_max - y_min), y_max + 0.05 * (y_max - y_min)]
        elif y_max <= 0:  # Negative values only
            y_range = [y_min - 0.05 * (y_max - y_min), y_max + 0.05 * (y_max - y_min)]
        else:  # Mixed positive and negative values
            y_range = [y_min - 0.05 * abs(y_min), y_max + 0.05 * abs(y_max)]

        fig = px.bar(df, x='Year', y=y_column,
                     title=title,
                     color_discrete_sequence=[color],
                     height=375)
        fig.update_traces(marker_line_width=0)
        fig.update_layout(
            yaxis=dict(range=y_range),
            plot_bgcolor='#2f2f2f',
            paper_bgcolor='#2f2f2f',
            font=dict(color='white'),
            margin=dict(l=20, r=20, t=60, b=40),
            autosize=True
        )
        return fig

    def create_data_table(df, y_column):
        table_html = "<table class='data-table'>"
        table_html += "<tr><th>Year</th>" + "".join([f"<th>{year}</th>" for year in df['Year']]) + "</tr>"
        table_html += f"<tr><td>{y_column}</td>"
        for value in df[y_column]:
            if value is not None:
                table_html += f"<td>{value:.2f}</td>"  # Format as a float with 2 decimal places
            else:
                table_html += "<td>N/A</td>"  # Use "N/A" for None values
        table_html += "</tr></table>"
        return table_html

    # Create all dataframes
    charts_data = [
        ("GDP Growth (%)", [report.get(f'GDPGrowthRateYear{i}', 0) for i in range(1, 7)], color_palette[0]),
        ("Inflation Rate (%)", [report.get(f'InflationYear{i}', 0) for i in range(1, 7)], color_palette[1]),
        ("Unemployment Rate (%)", [report.get(f'UnemploymentRateYear{i}', 0) for i in range(1, 7)], color_palette[2]),
        ("Population (millions)", [report.get(f'PopulationYear{i}', 0) for i in range(1, 7)], color_palette[3]),
        ("Government Budget Balance (% of GDP)", [report.get(f'GovernmentFinancesYear{i}', 0) for i in range(1, 7)], color_palette[4]),
        ("Current Account Balance (% of GDP)", [report.get(f'CurrentAccountBalanceYear{i}', 0) for i in range(1, 7)], color_palette[5])
    ]

    years = [2024, 2025, 2026, 2027, 2028, 2029]

    for metric, values, color in charts_data:
        df = pd.DataFrame({
            "Year": years,
            metric: values
        })

        # Display the chart with the specified color
        st.plotly_chart(plot_chart(df, metric, metric, color), use_container_width=True)

        # Display the data table
        st.markdown(create_data_table(df, metric), unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


