import streamlit as st
import pandas as pd
import plotly.express as px
import io

@st.cache_data
def load_data():
    df = pd.read_csv('vgsales.csv')
    return df

data = load_data()

st.title('Video Game Dashboard')
st.write('Explore video game sales, rating, and play')

# filtering data
if st.checkbox('Show raw data'):
    st.subheader('Raw Data')
    st.dataframe(data)
   
    # Create a sample DataFram
    df = pd.DataFrame(data)
    # Download the DataFrame as a CSV file

    # Create a StringIO object to hold the CSV data
    csv_buffer = io.StringIO()

    # Write the contents of the DataFrame to the StringIO object in CSV format
    # The index column is excluded from the output by passing index=False
    df.to_csv(csv_buffer, index=False)

    # Get the contents of the StringIO object as a string
    csv_data = csv_buffer.getvalue()

    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="sample_data.csv",
        mime="text/csv"
    )

# filter data 
platforms = data['Platform'].unique()
platforms_filter = st.multiselect('Selec platforms:',platforms, default=platforms)
filtered_data = data[data['Platform'].isin(platforms_filter)]

st.subheader("Top N Games by Global Sales")
top_n = st.number_input("Select the top N games:", min_value=5, max_value=100, value=10, step=1)
top_games = filtered_data.nlargest(top_n, "Global_Sales")
fig = px.bar(top_games, x="Name", y="Global_Sales", color="Platform", hover_name="Name", text="Global_Sales")
st.plotly_chart(fig)


st.subheader("Platform Market Share")
platform_share = filtered_data.groupby("Platform")["Global_Sales"].sum().reset_index()
fig2 = px.pie(platform_share, names="Platform", values="Global_Sales", title="Platform Market Share")
st.plotly_chart(fig2)

# Scatter plot for Year vs. Global Sales
st.subheader("Year vs. Global Sales")
fig3 = px.scatter(filtered_data, x="Year", y="Global_Sales", color="Platform", hover_name="Name", opacity=0.6)
st.plotly_chart(fig3)