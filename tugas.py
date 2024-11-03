import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

sns.set_palette("deep")

# Load dataset
hour_df = pd.read_csv("main_data.csv")
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

st.header('Insights Analisis Data: Bike Sharing Dataset')

# Total riders summary
col1, col2 = st.columns(2)
with col1:
    total_registered = hour_df.registered.sum()
    st.metric("Total pengendara terdaftar", value=total_registered)

with col2:
    total_casual = hour_df.casual.sum()
    st.metric("Total pengendara casual", value=total_casual)

# Create clusters based on temperature and humidity
hour_df['temp_cluster'] = pd.cut(hour_df['temp'], bins=3, labels=['Low', 'Medium', 'High'])
hour_df['hum_cluster'] = pd.cut(hour_df['hum'], bins=3, labels=['Low', 'Medium', 'High'])
hour_df['weather_cluster'] = hour_df['temp_cluster'].astype(str) + '_' + hour_df['hum_cluster'].astype(str)

# Clustering visualization
st.subheader('Clustering Berdasarkan Temperatur dan Kelembaban')
fig3, ax = plt.subplots(figsize=(10, 6))
for cluster in hour_df['weather_cluster'].unique():
    cluster_data = hour_df[hour_df['weather_cluster'] == cluster]
    ax.scatter(cluster_data['temp'], 
              cluster_data['hum'], 
              label=cluster, 
              alpha=0.6)
ax.set_xlabel('Temperatur')
ax.set_ylabel('Kelembaban')
ax.set_title('Clustering Berdasarkan Temperatur dan Kelembaban')
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
st.pyplot(fig3)

st.write("""
### Analisis Clustering:
Berdasarkan analisis data, kondisi cuaca dengan temperatur tinggi dan kelembaban rendah (High_Low) terbukti mendukung aktivitas penyewaan lebih optimal.
""")

if st.checkbox('Tampilkan Statistik Cluster'):
    st.write("### Statistik per Cluster")
    cluster_stats = hour_df.groupby('weather_cluster')['cnt'].agg(['count', 'mean', 'std']).round(2)
    cluster_stats.columns = ['Jumlah Data', 'Rata-rata Penyewaan', 'Standar Deviasi']
    st.dataframe(cluster_stats)

# Weather and season impact on casual vs registered riders
st.subheader('Dampak Cuaca dan Musim pada Pengendara Biasa vs Terdaftar')

# Sidebar filter options
weather_options = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca",
    options=hour_df['weathersit'].unique(),
    default=hour_df['weathersit'].unique()
)

season_options = st.sidebar.multiselect(
    "Pilih Musim",
    options=hour_df['season'].unique(),
    default=hour_df['season'].unique()
)

# Filter data
weather_data = hour_df[hour_df['weathersit'].isin(weather_options)].groupby('weathersit')[['casual', 'registered']].mean()
season_data = hour_df[hour_df['season'].isin(season_options)].groupby('season')[['casual', 'registered']].mean()

# Weather impact chart
st.subheader('Pengaruh Kondisi Cuaca pada Pengendara')
fig2, ax = plt.subplots(figsize=(12, 6))
labels_weather = ['Cerah', 'Berawan', 'Hujan Ringan', 'Hujan Lebat']
x = np.arange(len(labels_weather))
width = 0.35
ax.bar(x - width/2, weather_data['casual'], width, label='Pengendara Biasa', color='#ff9999')
ax.bar(x + width/2, weather_data['registered'], width, label='Pengendara Terdaftar', color='#66b3ff')
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Rata-rata Jumlah Pengendara')
ax.set_title('Perbandingan Jumlah Pengendara Berdasarkan Kondisi Cuaca')
ax.set_xticks(x)
ax.set_xticklabels(labels_weather, rotation=45)
ax.legend()
for i, v in enumerate(weather_data['casual']):
    ax.text(i - width/2, v, f'{v:.1f}', ha='center', va='bottom')
for i, v in enumerate(weather_data['registered']):
    ax.text(i + width/2, v, f'{v:.1f}', ha='center', va='bottom')
plt.tight_layout()
st.pyplot(fig2)

st.write("""
### Analisis Kondisi Cuaca:
Cuaca buruk memiliki dampak lebih besar pada pengendara kasual dibandingkan pengendara terdaftar.
""")

# Season impact chart
st.subheader('Pengaruh Musim pada Pengendara')
fig4, ax = plt.subplots(figsize=(12, 6))
labels_season = ['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin']
x = np.arange(len(labels_season))
width = 0.35
ax.bar(x - width/2, season_data['casual'], width, label='Pengendara Biasa', color='#ff9999')
ax.bar(x + width/2, season_data['registered'], width, label='Pengendara Terdaftar', color='#66b3ff')
ax.set_xlabel('Musim')
ax.set_ylabel('Rata-rata Jumlah Pengendara')
ax.set_title('Perbandingan Jumlah Pengendara Berdasarkan Musim')
ax.set_xticks(x)
ax.set_xticklabels(labels_season, rotation=45)
ax.legend()
for i, v in enumerate(season_data['casual']):
    ax.text(i - width/2, v, f'{v:.1f}', ha='center', va='bottom')
for i, v in enumerate(season_data['registered']):
    ax.text(i + width/2, v, f'{v:.1f}', ha='center', va='bottom')
plt.tight_layout()
st.pyplot(fig4)

st.write(""" 
### Analisis Clustering:
Perubahan musim memiliki dampak yang terbatas, tetapi musim semi cenderung mengalami penurunan jumlah pengendara.
""")

# Month analysis
st.subheader('Bulan Tersibuk untuk Penyewaan Sepeda: Hari Kerja vs Akhir Pekan')
fig, ax = plt.subplots(figsize=(10, 6))
month_weekday = hour_df[hour_df['workingday'] == 1].groupby('mnth')['cnt'].mean()
month_weekend = hour_df[hour_df['workingday'] == 0].groupby('mnth')['cnt'].mean()
sns.lineplot(x=month_weekday.index, y=month_weekday.values, label='Weekday', marker='o')
sns.lineplot(x=month_weekend.index, y=month_weekend.values, label='Weekend', marker='o')
ax.set_xlabel('Bulan (1: Januari, 12: Desember)')
ax.set_ylabel('Jumlah Rata-rata Pengendara')
ax.set_title('Bulan Tersibuk untuk Penyewaan Sepeda: Hari Kerja vs Akhir Pekan')
st.pyplot(fig)

st.write("""    
### Analisis Bulanan:
Musim panas dan musim gugur adalah periode puncak penyewaan sepeda.
""")
