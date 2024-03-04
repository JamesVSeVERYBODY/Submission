import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')
st.set_option('deprecation.showPyplotGlobalUse', False)

def daycount_df(day_df):
    filtered_df = day_df[(day_df['date'] >= "2011-01-01") & (day_df['date'] < "2012-12-31")]
    return filtered_df

def sales_performance_df(day_df):
    performance_df = day_df.groupby(by=["year", "month"]).agg({'count': 'sum'}).reset_index()
    return performance_df

def weather_count_df(day_df):
    weather_df = day_df.groupby(by='weather').agg({'count': 'sum'}).reset_index().sort_values(by='count', ascending=True)
    return weather_df

def daily_user_counts_df(day_df):
    user_counts_df = day_df.groupby(by=['days']).agg({
        'casual': 'sum',
        'registered': 'sum',
        'count': 'sum'
    }).reset_index()
    return user_counts_df

def hourly_user_counts_df(hour_df):
    user_counts_df = hour_df.groupby(by=['hour']).agg({
        'casual': 'sum',
        'registered': 'sum',
        'count': 'sum'
    }).reset_index()
    return user_counts_df

def user_counts_by_working_day_df(day_df):
    working_day_counts = day_df.groupby(by='workingday')['count'].sum().reset_index()
    return working_day_counts

def registered_df(day_df):
    reg_df = day_df.groupby('date')['registered'].sum().reset_index()
    reg_df.rename(columns={"registered": "register_sum"}, inplace=True)
    return reg_df

def casual_df(day_df):
    cas_df = day_df.groupby('date')['casual'].sum().reset_index()
    cas_df.rename(columns={"casual": "casual_sum"}, inplace=True)
    return cas_df

days_df = pd.read_csv("dashboard/day_clean.csv")
hours_df = pd.read_csv("dashboard/hour_clean.csv")

datetime_columns = ["date"]
days_df.sort_values(by="date", inplace=True)
days_df.reset_index(inplace=True)   

hours_df.sort_values(by="date", inplace=True)
hours_df.reset_index(inplace=True)

for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])
    hours_df[column] = pd.to_datetime(hours_df[column])

min_date_days = days_df["date"].min()
max_date_days = days_df["date"].max()

min_date_hour = hours_df["date"].min()
max_date_hour = hours_df["date"].max()

with st.sidebar:
    st.image("https://raw.githubusercontent.com/JamesVSeVERYBODY/ALLGAMBAR/main/logo.png")

    start_date, end_date = st.date_input(
        label='Date Filter :',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])
  
main_df_days = days_df[(days_df["date"] >= str(start_date)) & 
                       (days_df["date"] <= str(end_date))]

main_df_hour = hours_df[(hours_df["date"] >= str(start_date)) & 
                        (hours_df["date"] <= str(end_date))]

day_df_count_2011 = daycount_df(main_df_days)
reg_df = registered_df(main_df_days)
cas_df = casual_df(main_df_days)

st.header(":fax: Cycle Glide :bike:")
st.write("Cycle Glide: Ride Smooth, Ride Green!" ':herb:')
col1, col2, col3 = st.columns(3)
 
with col1:
    total_orders = day_df_count_2011['count'].sum()
    st.metric("Total Rides:man-biking:", value=total_orders)

with col2:
    total_sum = reg_df['register_sum'].sum()
    st.metric("Total Registered Rides	:registered:", value=total_sum)

with col3:
    total_sum = cas_df['casual_sum'].sum()
    st.metric("Total Casual Rides	:shirt:", value=total_sum)


st.subheader("Company Sales Performance in Recent Years")
performance_data = sales_performance_df(main_df_days)

plt.figure(figsize=(12, 6))
plt.plot(performance_data.index, performance_data['count'], marker='o', linestyle='-', color='yellow', alpha=1, markerfacecolor='grey', label='Sales Performance')
plt.title('Monthly Total Count Distribution (2011 - 2012)')
plt.xticks(range(len(performance_data)), performance_data['month'], rotation=45)
plt.grid(True, axis='y', linestyle='--', color='white', linewidth=0.2)
plt.gca().patch.set_facecolor('#0E1117')

plt.legend()

plt.show()
st.pyplot()

st.subheader("Number of Users Based on Weather")
weather_data = weather_count_df(main_df_days)

plt.figure(figsize=(12, 6))
sns.pointplot(x=weather_data['weather'].str.slice(0, 22), y='count', data=weather_data, marker='o', linestyle='-', color='yellow', alpha=1, markerfacecolor='black', label='User Count')
plt.ylabel('User Count (Mil)')
plt.xticks(rotation=0)
plt.grid(True, axis='y', linestyle='--', color='white',linewidth=0.2)
plt.gca().patch.set_facecolor('#0E1117')

plt.legend()

plt.show()
st.pyplot()


st.subheader("Number of Users Based on Days")
user_counts_data = daily_user_counts_df(main_df_days)

plt.figure(figsize=(10, 6))
plt.bar(user_counts_data['days'], user_counts_data['casual'], label='Casual', alpha=0.7, color='#ACCDCD')
plt.bar(user_counts_data['days'], user_counts_data['registered'], bottom=user_counts_data['casual'], label='Registered', alpha=0.7, color='#2E4D4A')
plt.legend()

plt.gca().patch.set_facecolor('#0E1117')

plt.show()
st.pyplot()


st.subheader("User Distribution per Hour")
user_counts_hourly_data = hourly_user_counts_df(main_df_hour)

plt.figure(figsize=(10, 6))
bar_width = 0.3
index = user_counts_hourly_data['hour']

plt.bar(index - bar_width, user_counts_hourly_data['casual'], bar_width, label='Casual', color='#ACCDCD', alpha=1)
plt.bar(index, user_counts_hourly_data['registered'], bar_width, label='Registered', color='#315252', alpha=1)
plt.bar(index + bar_width, user_counts_hourly_data['count'], bar_width, label='Total', color='#B7BEC0', alpha=1)

plt.xlabel('Notes : 0 = 1, 23 = 24')
plt.xticks(index)
plt.legend()

# Set background color and spines color
plt.gca().patch.set_facecolor('#0E1117')

plt.grid(False)
st.pyplot()


st.subheader("Percentage of Users Based on Workdays")
working_day_counts_data = user_counts_by_working_day_df(main_df_days)

plt.figure(figsize=(8, 8))
colors = ['#9CDCD4','#20535D','#D4BCA4','#462F1B'] 
plt.pie(working_day_counts_data['count'], labels=working_day_counts_data['workingday'], autopct='%1.1f%%', startangle=140, colors=colors, wedgeprops={'edgecolor': 'white'})
plt.axis('equal')
plt.tight_layout()
st.pyplot()

satisfaction_level = st.sidebar.radio(
    label="Select Satisfaction Level",
    options=('Low', 'Medium', 'High'),
    index=1
)

st.sidebar.subheader("Contact Me")
st.sidebar.markdown("[LinkedIn](https://linkedin.com/in/james-philip-a7475a190/)")
st.sidebar.markdown("[GitHub](https://github.com/JamesVSEverybody)")

st.header("End of Document")
name = st.text_input(label='Username', value='')
text = st.text_area('If you have any words to say , tyep here :')

st.sidebar.caption("Copyright © 2024 All Rights Reserved [James Philip]")