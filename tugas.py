import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

sns.set_palette("deep")

# Load data
hour_df = pd.read_csv("main_data.csv")
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Header
st.header('Insights Analisis Data: Bike Sharing Dataset')

# Metric Columns
col1, col2 = st.columns(2)
with col1:
    total_registered = hour_df.registered.sum()
    st.metric("Total pengendara terdaftar", value=total_registered)
with col2:
    total_casual = hour_df.casual.sum()
    st.metric("Total pengendara casual", value=total_casual)

# Cluster Based on Temperature and Humidity
hour_df['temp_cluster'] = pd.cut(hour_df['temp'], bins=3, labels=['Low', 'Medium', 'High'])
hour_df['hum_cluster'] = pd.cut(hour_df['hum'], bins=3, labels=['Low', 'Medium', 'High'])
hour_df['weather_cluster'] = hour_df['temp_cluster'].astype(str) + '_' + hour_df['hum_cluster'].astype(str)

# Dropdown to Select Cluster
st.subheader('Clustering Berdasarkan Temperatur dan Kelembaban')
selected_cluster = st.selectbox("Pilih Cluster Cuaca:", ['All'] + list(hour_df['weather_cluster'].unique()))

if selected_cluster == 'All':
    # Show all clusters in a scatter plot
    fig3, ax = plt.subplots(figsize=(10, 6))
    for cluster in hour_df['weather_cluster'].unique():
        cluster_data = hour_df[hour_df['weather_cluster'] == cluster]
        ax.scatter(cluster_data['temp'], cluster_data['hum'], label=cluster, alpha=0.6)
    ax.set_xlabel('Temperatur')
    ax.set_ylabel('Kelembaban')
    ax.set_title('Clustering Berdasarkan Temperatur dan Kelembaban')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(fig3)
else:
    # Filter data berdasarkan cluster yang dipilih
    filtered_data = hour_df[hour_df['weather_cluster'] == selected_cluster]

    # Tampilkan data dalam bentuk bar chart untuk jumlah pengendara
    fig, ax = plt.subplots(figsize=(8, 6))
    casual_mean = filtered_data['casual'].mean()
    registered_mean = filtered_data['registered'].mean()
    ax.bar(['Casual', 'Registered'], [casual_mean, registered_mean], color=['#ff9999', '#66b3ff'])
    ax.set_ylabel('Rata-rata Jumlah Pengendara')
    ax.set_title(f'Rata-rata Pengendara di Cluster {selected_cluster}')
    for i, v in enumerate([casual_mean, registered_mean]):
        ax.text(i, v, f'{v:.1f}', ha='center', va='bottom')
    st.pyplot(fig)

# Display Explanation
st.write("""
### Analisis Clustering:
Berdasarkan analisis data, kondisi cuaca dengan temperatur tinggi dan kelembaban rendah (High_Low) terbukti cuaca hangat dan kering paling optimal untuk mendukung aktivitas penyewaan.
""")

# Show Cluster Statistics Optionally
if st.checkbox('Tampilkan Statistik Cluster'):
    st.write("### Statistik per Cluster")
    cluster_stats = hour_df.groupby('weather_cluster')['cnt'].agg(['count', 'mean', 'std']).round(2)
    cluster_stats.columns = ['Jumlah Data', 'Rata-rata Penyewaan', 'Standar Deviasi']
    st.dataframe(cluster_stats)




# Siapkan data
season_data = hour_df.groupby('season')[['casual', 'registered']].mean()
st.subheader(' dampak musim dan musim pada pengendara biasa vs pengendara terdaftar')
# Buat figure menggunakan matplotlib
fig4, ax = plt.subplots(figsize=(12, 6))

# Definisikan labels untuk musim
labels_season = ['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin']

# Buat bar chart
x = np.arange(len(labels_season))
width = 0.35

ax.bar(x - width/2, season_data['casual'], width, label='Pengendara Biasa', color='#ff9999')
ax.bar(x + width/2, season_data['registered'], width, label='Pengendara Terdaftar', color='#66b3ff')

# Kustomisasi grafik
ax.set_xlabel('Musim')
ax.set_ylabel('Rata-rata Jumlah Pengendara')
ax.set_title('Perbandingan Jumlah Pengendara Berdasarkan Musim')
ax.set_xticks(x)
ax.set_xticklabels(labels_season, rotation=45)
ax.legend()

# Tambahkan nilai di atas bar
for i, v in enumerate(season_data['casual']):
    ax.text(i - width/2, v, f'{v:.1f}', ha='center', va='bottom')
for i, v in enumerate(season_data['registered']):
    ax.text(i + width/2, v, f'{v:.1f}', ha='center', va='bottom')

plt.tight_layout()

# Tampilkan plot di Streamlit
st.pyplot(fig4)

st.write(""" 
    ### Analisis Clustering:
    Kondisi musim berdampak tapi tidak terlalu signifikan mempengaruhi 
    pengendara kasual ataupun pengendara yang terdaftar. Hanya pada musim 
    semi pengendara cukup mengalami menurunan.
    """
    )

# Visualisasi 
st.subheader(' dampak cuaca dan musim pada pengendara biasa vs pengendara terdaftar')

# Siapkan data
weather_data = hour_df.groupby('weathersit')[['casual', 'registered']].mean()

# Buat figure baru
fig2, ax = plt.subplots(figsize=(12, 6))

# Definisikan labels untuk kondisi cuaca
labels_weather = ['Cerah', 'Berawan', 'Hujan Ringan', 'Hujan Lebat']

# Buat bar chart
x = np.arange(len(labels_weather))
width = 0.35

ax.bar(x - width/2, weather_data['casual'], width, label='Pengendara Biasa', color='#ff9999')
ax.bar(x + width/2, weather_data['registered'], width, label='Pengendara Terdaftar', color='#66b3ff')

# Kustomisasi grafik
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Rata-rata Jumlah Pengendara')
ax.set_title('Perbandingan Jumlah Pengendara Berdasarkan Kondisi Cuaca')
ax.set_xticks(x)
ax.set_xticklabels(labels_weather, rotation=45)
ax.legend()

# Tambahkan nilai di atas bar
for i, v in enumerate(weather_data['casual']):
    ax.text(i - width/2, v, f'{v:.1f}', ha='center', va='bottom')
for i, v in enumerate(weather_data['registered']):
    ax.text(i + width/2, v, f'{v:.1f}', ha='center', va='bottom')

plt.tight_layout()

# Tampilkan plot di Streamlit
st.pyplot(fig2)

# Tambahkan penjelasan
st.write("""
### Analisis Kondisi Cuaca:
Kondisi cuaca secara signifikan mempengaruhi pengendara kasual 
lebih banyak daripada pengendara yang terdaftar.Jumlah rata-rata 
pengendara kasual menurun secara signifikan saat cuaca memburuk sebanyak.
""")


st.subheader('bulan tersibuk untuk penyewaan sepeda, dengan membandingkan Weekday dan Weekend')
# Visualisasikan bulan tersibuk untuk penyewaan sepeda, dengan membandingkan Weekday dan Weekend
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
    ### Analisis Clustering:
    Bulan-bulan musim gugur dan panas adalah 
    periode puncak untuk penyewaan sepeda, terlepas 
     dari weekend atau weekday.
    """
)
