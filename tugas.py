# Import yang dibutuhkan
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_palette("deep")

# Load data
hour_df = pd.read_csv("main_data.csv")
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

st.header('Insights Analisis Data: Bike Sharing Dataset')

# Filter Clustering Berdasarkan Temperatur dan Kelembaban
st.subheader('Clustering Berdasarkan Temperatur dan Kelembaban (dengan Filter)')
# Filter cluster cuaca
cluster_option = st.selectbox('Pilih Cluster Cuaca:', hour_df['weather_cluster'].unique(), index=0)
filtered_data = hour_df[hour_df['weather_cluster'] == cluster_option]

# Visualisasi clustering dengan filter
fig, ax = plt.subplots(figsize=(10, 6))
for cluster in filtered_data['weather_cluster'].unique():
    cluster_data = filtered_data[filtered_data['weather_cluster'] == cluster]
    ax.scatter(cluster_data['temp'], 
               cluster_data['hum'], 
               label=cluster, 
               alpha=0.6)

# Kustomisasi grafik
ax.set_xlabel('Temperatur')
ax.set_ylabel('Kelembaban')
ax.set_title('Clustering Berdasarkan Temperatur dan Kelembaban (Filtered)')
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
st.pyplot(fig)

# Filter pada chart Kondisi Cuaca
st.subheader('Perbandingan Jumlah Pengendara Berdasarkan Kondisi Cuaca (dengan Filter)')
weather_option = st.selectbox('Pilih Kondisi Cuaca:', hour_df['weathersit'].unique())
weather_data = hour_df[hour_df['weathersit'] == weather_option].groupby('weathersit')[['casual', 'registered']].mean()

fig2, ax = plt.subplots(figsize=(12, 6))
labels_weather = ['Cerah', 'Berawan', 'Hujan Ringan', 'Hujan Lebat']
x = np.arange(len(labels_weather))
width = 0.35

ax.bar(x - width/2, weather_data['casual'], width, label='Pengendara Biasa', color='#ff9999')
ax.bar(x + width/2, weather_data['registered'], width, label='Pengendara Terdaftar', color='#66b3ff')

# Kustomisasi grafik
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Rata-rata Jumlah Pengendara')
ax.set_title(f'Perbandingan Jumlah Pengendara Berdasarkan Kondisi Cuaca: {weather_option}')
ax.set_xticks(x)
ax.set_xticklabels(labels_weather, rotation=45)
ax.legend()

plt.tight_layout()
st.pyplot(fig2)

# Filter pada chart Berdasarkan Musim
st.subheader('Perbandingan Jumlah Pengendara Berdasarkan Musim (dengan Filter)')
season_option = st.selectbox('Pilih Musim:', hour_df['season'].unique())
season_data = hour_df[hour_df['season'] == season_option].groupby('season')[['casual', 'registered']].mean()

fig4, ax = plt.subplots(figsize=(12, 6))
labels_season = ['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin']
x = np.arange(len(labels_season))
width = 0.35

ax.bar(x - width/2, season_data['casual'], width, label='Pengendara Biasa', color='#ff9999')
ax.bar(x + width/2, season_data['registered'], width, label='Pengendara Terdaftar', color='#66b3ff')

# Kustomisasi grafik
ax.set_xlabel('Musim')
ax.set_ylabel('Rata-rata Jumlah Pengendara')
ax.set_title(f'Perbandingan Jumlah Pengendara Berdasarkan Musim: {season_option}')
ax.set_xticks(x)
ax.set_xticklabels(labels_season, rotation=45)
ax.legend()

plt.tight_layout()
st.pyplot(fig4)
