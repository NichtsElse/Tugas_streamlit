import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_palette("deep")

hour_df = pd.read_csv("hour.csv")

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
    
weather_casual = hour_df.groupby('weathersit')['casual'].mean()
weather_registered = hour_df.groupby('weathersit')['registered'].mean()
fig, ax = plt.subplots(figsize=(10, 6))


sns.barplot(x=weather_casual.index, y=weather_casual.values, color='b', label='Casual')
sns.barplot(x=weather_registered.index, y=weather_registered.values, color='r', label='Registered', alpha=0.6)

ax.set_xlabel('Situasi Cuaca')
ax.set_ylabel('Jumlah Rata-rata Pengendara')
ax.set_title('Jumlah Rata-rata Pengendara berdasarkan Situasi Cuaca')
ax.set_xticklabels(['Clear', 'Kabut', 'hujan/Salju Ringan', 'Hujan/Salju Lebat'], rotation=45)
st.pyplot(fig)
with st.expander("See explanation"):
    st.write(
        """kondisi cuaca secara signifikan mempengaruhi pengendara 
        kasual lebih banyak daripada pengendara yang terdaftar.Jumlah 
        rata-rata pengendara kasual menurun secara signifikan saat cuaca memburuk 
        sebanyak.
        """
    )

season_casual = hour_df.groupby('season')['casual'].mean()
season_registered = hour_df.groupby('season')['registered'].mean()
fig, ax = plt.subplots(figsize=(10, 6))

sns.barplot(x=season_casual.index, y=season_casual.values, color='b', label='Casual')
sns.barplot(x=season_registered.index, y=season_registered.values, color='r', label='Registered', alpha=0.6)

ax.set_xlabel('Musim')
ax.set_ylabel('Jumlah Rata-rata Pengendara')
ax.set_title('Jumlah Rata-rata Pengendara berdasarkan Musim')
ax.set_xticklabels(['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'], rotation=45)
st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
        """Kondisi musim berdampak tapi tidak terlalu signifikan mempengaruhi 
        pengendara kasual ataupun pengendara yang terdaftar. Hanya pada musim 
        semi pengendara cukup mengalami menurunan.
        """
    )

# Visualisasikan bulan tersibuk untuk penyewaan sepeda, dengan membandingkan Weekday dan Weekend
fig, ax = plt.subplots(figsize=(10, 6))
month_weekday = hour_df[hour_df['workingday'] == 1].groupby('mnth')['cnt'].mean()
month_weekend = hour_df[hour_df['workingday'] == 0].groupby('mnth')['cnt'].mean()

sns.lineplot(x=month_weekday.index, y=month_weekday.values, label='Weekday', marker='o')
sns.lineplot(x=month_weekend.index, y=month_weekend.values, label='Weekend', marker='o')

st.subheader('Hourly Trend of Bike Rentals')
ax.set_xlabel('Bulan (1: Januari, 12: Desember)')
ax.set_ylabel('Jumlah Rata-rata Pengendara')
ax.set_title('Bulan Tersibuk untuk Penyewaan Sepeda: Hari Kerja vs Akhir Pekan')
st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
        """ Bulan-bulan musim gugur dan panas adalah 
        periode puncak untuk penyewaan sepeda, terlepas 
        dari weekend atau weekday.
        """
    )