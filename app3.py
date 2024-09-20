
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    file = "./aircrashes.csv"
    df = pd.read_csv(file)
        
    df = df.dropna(axis = 0)
    df.rename(columns={'Country/Region':'Region'},
           inplace =True)
    df.loc[:, 'Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']].astype(str).agg('-'.join, axis=1), errors='coerce')
    df['Survivor Rate (%)'] = df['Fatalities (air)'] / df['Aboard'] * 100

    # Define the correct order of months
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    # Ensure the 'Month' column is treated as a categorical variable with the correct order
    df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)

    return df
    return df.head(100)


df = load_data()

st.set_page_config(page_title = "Dashboard", layout="wide")
st.subheader("✈️ Aircrash Trends and Analysis (1902–2023)")
st.markdown('##')

st.write(df)


 # Sidebar filters
st.sidebar.header("Please Filter")

# Years filter
years = df['Year'].unique()
selected_years = st.sidebar.multiselect("Select Years", years, default=years)


# Filter Dataframe based on selection
filtered_df = df[df['Year'].isin(selected_years)]


# display metrics

number_of_crashes = df['Aircraft'].count()
ground_fatalities = df['Ground'].sum()
air_fatalities = df['Fatalities (air)'].sum()
total_fatalities = air_fatalities + ground_fatalities


col1, col2, col3, col4 = st.columns(4)

with col4:
    st.info('Casualties on Land', icon ='📌')
    st.metric(label='on Land', value=f"{ground_fatalities:,}")


with col3:
    st.info('Casualties in Air', icon ='📌')
    st.metric(label='in Air', value=f"{air_fatalities:,}")

with col2:
    st.info('Total Casualties', icon ='📌')
    st.metric(label='Casualties', value=f"{total_fatalities:,}")


with col1:
    st.info('Airplane Crashes', icon ='📌')
    st.metric(label='Crashes', value=f"{number_of_crashes:,}")


st.subheader("Deep Dive")


# 1. Crashes per Year (Line Chart)
crashes_per_year = df.groupby('Year').size().reset_index(name='Crashes by Year')
fig1, ax1 = plt.subplots(figsize=(12, 6))
ax1.plot(crashes_per_year['Year'], crashes_per_year['Crashes by Year'], marker='o', linestyle='-', color = 'red')
ax1.set_xlabel('Year')
ax1.set_ylabel('Number of Crashes')
ax1.set_title('Crashes per Year')
ax1.grid(True)

# 2. Crashes per Aircraft Type (Horizontal Bar Chart)
crashes_per_aircraft = df.groupby('Aircraft').size().reset_index(name='Number of Crashes')
crashes_per_aircraft_sorted = crashes_per_aircraft.sort_values(by='Number of Crashes', ascending=False)
top_10_crashes = crashes_per_aircraft_sorted.head(10)
fig2, ax2 = plt.subplots(figsize=(12, 6))
ax2.barh(top_10_crashes['Aircraft'], top_10_crashes['Number of Crashes'], color='gray')
ax2.set_xlabel('Number of Crashes')
ax2.set_ylabel('Aircraft Type')
ax2.set_title('Crashes per Model')
ax2.grid(True)

# 3. Crashes per Country (Horizontal Bar Chart)
crashes_per_region = df.groupby('Region').size().reset_index(name='Crashes by Region')
crashes_per_region_sorted = crashes_per_region.sort_values(by='Crashes by Region', ascending=False)
top_10_region = crashes_per_region_sorted.head(10)
fig3, ax3 = plt.subplots(figsize=(12, 6))
ax3.barh(top_10_region['Region'], top_10_region['Crashes by Region'], color='teal')
ax3.set_xlabel('Number of Crashes')
ax3.set_ylabel('Region')
ax3.set_title('Crashes per Country')
ax3.grid(True)

# 4. Fatalities by Month (Line Chart)
monthly_fatalities = df.groupby('Month')['Aircraft'].count().reset_index(name='Casualties by Month')
fig4, ax4 = plt.subplots(figsize=(14, 7))
ax4.plot(monthly_fatalities['Month'], monthly_fatalities['Casualties by Month'], marker='o', linestyle='-', color='orange')
ax4.set_title('Crashes per Month')
ax4.set_xlabel('Month')
ax4.set_ylabel('Total Crashes')
ax4.grid(True)
ax4.set_xticklabels(monthly_fatalities['Month'])

# Display the plots in a 2x2 grid
col1, col2 = st.columns(2)
with col1:
    st.pyplot(fig1)
    st.pyplot(fig2)
with col2:
    st.pyplot(fig4)
    st.pyplot(fig3)






# Survivor Rate by Year

st.subheader('Evolution of Survivor Rates')
yearly_survivor_rate = df.groupby('Year')['Survivor Rate (%)'].mean().reset_index(name = 'Survivor Rate')

plt.figure(figsize=(14, 7))
plt.plot(yearly_survivor_rate['Year'], yearly_survivor_rate['Survivor Rate'], marker='o', linestyle='-')
plt.xlabel('Year')
plt.ylabel('Survivor Rate')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Show plot
st.pyplot(plt)