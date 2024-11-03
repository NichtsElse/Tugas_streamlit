import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

sns.set_palette("deep")

hour_df = pd.read_csv("main_data.csv")

hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

st.header('Insights Analisis Data: Bike Sharing Dataset')


st.subheader(' dampak cuaca dan musim pada pengendara biasa vs pengendara terdaftar')
col1, col2 = st.columns(2)
with col1:
    total_registered = hour_df.registered.sum()
    st.metric("Total pengendara terdaftar", value=total_registered)

with col2:
    total_casual = hour_df.casual.sum()
    st.metric("Total pengendara casual", value=total_casual)

# Tambahkan setelah visualisasi sebelumnya

# Buat cluster berdasarkan suhu dan kelembaban (pastikan kode ini dijalankan setelah load data)
hour_df['temp_cluster'] = pd.cut(hour_df['temp'], bins=3, labels=['Low', 'Medium', 'High'])
hour_df['hum_cluster'] = pd.cut(hour_df['hum'], bins=3, labels=['Low', 'Medium', 'High'])
hour_df['weather_cluster'] = hour_df['temp_cluster'].astype(str) + '_' + hour_df['hum_cluster'].astype(str)

# Visualisasi clustering
st.subheader('Clustering Berdasarkan Temperatur dan Kelembaban')

# Filter untuk cluster
cluster_option = st.selectbox('Pilih Cluster Cuaca:', hour_df['weather_cluster'].unique(), index=0)
filtered_data = hour_df[hour_df['weather_cluster'] == cluster_option]

# Visualisasi clustering berdasarkan pilihan filter
st.subheader('Clustering Berdasarkan Temperatur dan Kelembaban')

fig3, ax = plt.subplots(figsize=(10, 6))

# Plot scatter untuk cluster yang dipilih
ax.scatter(filtered_data['temp'], 
           filtered_data['hum'], 
           label=cluster_option, 
           alpha=0.6)

# Kustomisasi grafik
ax.set_xlabel('Temperatur')
ax.set_ylabel('Kelembaban')
ax.set_title(f'Clustering Berdasarkan Temperatur dan Kelembaban: {cluster_option}')
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
st.pyplot(fig3)

# Tambahkan penjelasan
st.write("""
### Analisis Clustering:
Berdasarkan analisis data, kondisi cuaca dengan temperatur tinggi dan
kelembaban rendah (High_Low) terbukti Cuaca Hangat dan Kering paling
optimal untuk mendukung aktivitas penyewaan. Kondisi ini diikuti oleh cuaca 
dengan temperatur tinggi dan kelembaban sedang (High_Medium) yang juga menunjukkan
performa baik. Sebaliknya, Cuaca dengan temperatur rendah, terutama yang disertai 
kelembaban tinggi (Low_High), cenderung berkontribusi pada angka penyewaan yang lebih 
rendah, kemungkinan disebabkan oleh kondisi yang kurang ideal untuk aktivitas luar ruangan.
""")

# Tambahkan statistik cluster
if st.checkbox('Tampilkan Statistik Cluster'):
    st.write("### Statistik per Cluster")
    cluster_stats = hour_df.groupby('weather_cluster')['cnt'].agg(['count', 'mean', 'std']).round(2)
    cluster_stats.columns = ['Jumlah Data', 'Rata-rata Penyewaan', 'Standar Deviasi']
    st.dataframe(cluster_stats)



# Filter untuk kondisi cuaca
weather_option = st.selectbox('Pilih Kondisi Cuaca:', labels_weather)
weather_filtered_data = hour_df[hour_df['weathersit'] == labels_weather.index(weather_option) + 1]

st.subheader('dampak cuaca pada pengendara kasual vs pengendara terdaftar')

fig2, ax = plt.subplots(figsize=(12, 6))

ax.bar(['Pengendara Biasa'], weather_filtered_data['casual'].mean(), color='#ff9999')
ax.bar(['Pengendara Terdaftar'], weather_filtered_data['registered'].mean(), color='#66b3ff')

# Kustomisasi grafik
ax.set_ylabel('Rata-rata Jumlah Pengendara')
ax.set_title(f'Jumlah Pengendara Berdasarkan Kondisi Cuaca: {weather_option}')
ax.legend(['Pengendara Biasa', 'Pengendara Terdaftar'])

st.pyplot(fig2)

# Tambahkan penjelasan
st.write("""
### Analisis Kondisi Cuaca:
Kondisi cuaca secara signifikan mempengaruhi pengendara kasual 
lebih banyak daripada pengendara yang terdaftar.Jumlah rata-rata 
pengendara kasual menurun secara signifikan saat cuaca memburuk sebanyak.
""")


st.subheader('dampak musim pada pengendara kasual vs pengendara terdaftar')
# Definisikan labels untuk musim di awal
labels_season = ['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin']
# Filter untuk musim
season_option = st.selectbox('Pilih Musim:', labels_season)
season_filtered_data = hour_df[hour_df['season'] == labels_season.index(season_option) + 1]

fig4, ax = plt.subplots(figsize=(12, 6))

ax.bar(['Pengendara Biasa'], season_filtered_data['casual'].mean(), color='#ff9999')
ax.bar(['Pengendara Terdaftar'], season_filtered_data['registered'].mean(), color='#66b3ff')

# Kustomisasi grafik
ax.set_ylabel('Rata-rata Jumlah Pengendara')
ax.set_title(f'Jumlah Pengendara Berdasarkan Musim: {season_option}')
ax.legend(['Pengendara Biasa', 'Pengendara Terdaftar'])

st.pyplot(fig4)

st.write(""" 
    ### Analisis Clustering:
    Kondisi musim berdampak tapi tidak terlalu signifikan mempengaruhi 
    pengendara kasual ataupun pengendara yang terdaftar. Hanya pada musim 
    semi pengendara cukup mengalami menurunan.
    """
    )


# Inisialisasi data untuk weekday dan weekend berdasarkan bulan
month_weekday = hour_df[hour_df['workingday'] == 1].groupby('mnth')['cnt'].mean()
month_weekend = hour_df[hour_df['workingday'] == 0].groupby('mnth')['cnt'].mean()

# Filter untuk hari kerja atau akhir pekan
day_option = st.selectbox('Pilih Jenis Hari:', ['Weekday', 'Weekend'])

st.subheader('bulan tersibuk untuk penyewaan sepeda')

fig, ax = plt.subplots(figsize=(10, 6))

if day_option == 'Weekday':
    month_data = month_weekday
else:
    month_data = month_weekend

sns.lineplot(x=month_data.index, y=month_data.values, marker='o')
ax.set_xlabel('Bulan (1: Januari, 12: Desember)')
ax.set_ylabel('Jumlah Rata-rata Pengendara')
ax.set_title(f'Bulan Tersibuk untuk Penyewaan Sepeda: {day_option}')

st.pyplot(fig)

st.write("""    
    ### Analisis Clustering:
    Bulan-bulan musim gugur dan panas adalah 
    periode puncak untuk penyewaan sepeda, terlepas 
     dari weekend atau weekday.
    """
)
