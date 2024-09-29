import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def get_total_count_by_hour_data(hour_data):
  hour_count_data =  hour_data.groupby(by="hours").agg({"count_cr": ["sum"]})
  return hour_count_data

def count_by_day_data(day_data):
    day_data_count_2011 = day_data.query(str('dteday >= "2011-01-01" and dteday < "2012-12-31"'))
    return day_data_count_2011

def total_registered_data(day_data):
   reg_data =  day_data.groupby(by="dteday").agg({
      "registered": "sum"
    })
   reg_data = reg_data.reset_index()
   reg_data.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
   return reg_data

def total_casual_data(day_data):
   cas_data =  day_data.groupby(by="dteday").agg({
      "casual": ["sum"]
    })
   cas_data = cas_data.reset_index()
   cas_data.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
   return cas_data

def sum_order (hour_data):
    sum_order_items_data = hour_data.groupby("one_of_week").count_cr.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_data

def macem_season (day_data): 
    season_data = day_data.groupby(by="season").count_cr.sum().reset_index() 
    return season_data

days_data = pd.read_csv("dashboard/day_clean.csv")
hours_data = pd.read_csv("dashboard/hour_clean.csv")

datetime_columns = ["dteday"]
days_data.sort_values(by="dteday", inplace=True)
days_data.reset_index(inplace=True)   

hours_data.sort_values(by="dteday", inplace=True)
hours_data.reset_index(inplace=True)

for column in datetime_columns:
    days_data[column] = pd.to_datetime(days_data[column])
    hours_data[column] = pd.to_datetime(hours_data[column])

min_date_days = days_data["dteday"].min()
max_date_days = days_data["dteday"].max()

min_date_hour = hours_data["dteday"].min()
max_date_hour = hours_data["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/image1_hH9B4gs.jpg")
    
        # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])
  
main_data_days = days_data[(days_data["dteday"] >= str(start_date)) & 
                       (days_data["dteday"] <= str(end_date))]

main_data_hour = hours_data[(hours_data["dteday"] >= str(start_date)) & 
                        (hours_data["dteday"] <= str(end_date))]

hour_count_data = get_total_count_by_hour_data(main_data_hour)
day_data_count_2011 = count_by_day_data(main_data_days)
reg_data = total_registered_data(main_data_days)
cas_data = total_casual_data(main_data_days)
sum_order_items_data = sum_order(main_data_hour)
season_data = macem_season(main_data_hour)

#Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header('Bike Sharing :sparkles:')

st.subheader('Daily Sharing')
col1, col2, col3 = st.columns(3)
 
with col1:
    total_orders = day_data_count_2011.count_cr.sum()
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    total_sum = reg_data.register_sum.sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = cas_data.casual_sum.sum()
    st.metric("Total Casual", value=total_sum)

st.subheader("Performa penjualan perusahaan dalam beberapa tahun terakhir")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    days_data["dteday"],
    days_data["count_cr"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.subheader("pada hari apa yang paling banyak dan paling sedikit disewa?")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(50, 20))

sns.barplot(x="one_of_week", y="count_cr", data=sum_order_items_data.head(5), palette=["#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3"], ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Day", fontsize=30)
ax[0].set_title("Hari dengan sedikit penyewa sepeda", loc="center", fontsize=30)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="one_of_week", y="count_cr", data=sum_order_items_data.sort_values(by="one_of_week", ascending=True).head(5), palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#90CAF9"], ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Day",  fontsize=30)
ax[1].set_title("Hari dengan banyak penyewa sepeda", loc="center", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)

st.subheader("Perbandingan Customer yang Registered dengan casual")

labels = 'casual', 'registered'
sizes = [18.8, 81.2]
explode = (0, 0.1) 

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',colors=["#D3D3D3", "#90CAF9"],
        shadow=True, startangle=90)
ax1.axis('equal')  

st.pyplot(fig1)
