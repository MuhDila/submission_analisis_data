import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
all_df = pd.read_csv("all_data.csv")

# Konversi kolom tanggal ke format datetime
all_df["dteday"] = pd.to_datetime(all_df["dteday"])

# Sidebar - Filter rentang tanggal
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    st.image("https://bikeshare.metro.net/wp-content/uploads/2016/04/cropped-metro-bike-share-favicon.png")
    start_date, end_date = st.date_input(
        "Pilih Rentang Tanggal",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    day_type = st.radio("Pilih Jenis Hari", ["Semua Hari", "Hari Kerja", "Akhir Pekan"])

# Filter data berdasarkan tanggal dan jenis hari
filtered_df = all_df[(all_df["dteday"] >= str(start_date)) & (all_df["dteday"] <= str(end_date))]
if day_type == "Hari Kerja":
    filtered_df = filtered_df[filtered_df["workingday_hour"] == 1]
elif day_type == "Akhir Pekan":
    filtered_df = filtered_df[filtered_df["workingday_hour"] == 0]

# Header
st.title("Bike Sharing Dashboard 🚴‍♂️")

# Section 1: Overview Data
st.subheader("Overview Data")
col1, col2 = st.columns(2)
with col1:
    total_rentals = filtered_df["cnt_hour"].sum()
    st.metric("Total Peminjaman Sepeda", total_rentals)
with col2:
    avg_rentals = round(filtered_df["cnt_hour"].mean(), 2)
    st.metric("Rata-rata Peminjaman per Hari", avg_rentals)

# Section 2: Pola Peminjaman Sepeda Berdasarkan Waktu
st.subheader("Pola Peminjaman Sepeda Berdasarkan Waktu")
hourly_rentals_weekday = filtered_df[filtered_df["workingday_hour"] == 1].groupby("hr")["cnt_hour"].mean()
hourly_rentals_weekend = filtered_df[filtered_df["workingday_hour"] == 0].groupby("hr")["cnt_hour"].mean()

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(hourly_rentals_weekday.index, hourly_rentals_weekday, marker='o', label="Hari Kerja", linestyle='-')
ax.plot(hourly_rentals_weekend.index, hourly_rentals_weekend, marker='s', label="Akhir Pekan", linestyle='--')
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Rata-rata Peminjaman Sepeda")
ax.set_title("Rata-rata Peminjaman Sepeda per Jam (Hari Kerja vs Akhir Pekan)")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Section 3: Faktor yang Berpengaruh terhadap Peminjaman Sepeda
st.subheader("Faktor yang Berpengaruh terhadap Peminjaman Sepeda")
correlation_matrix = filtered_df.corr(numeric_only=True)
correlation_with_cnt = correlation_matrix["cnt_hour"].drop("cnt_hour").sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=correlation_with_cnt.values, y=correlation_with_cnt.index, palette="coolwarm", ax=ax)
ax.set_xlabel("Korelasi dengan Jumlah Peminjaman Sepeda")
ax.set_ylabel("Variabel")
ax.set_title("Faktor yang Paling Berpengaruh terhadap Peminjaman Sepeda")
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5, ax=ax)
ax.set_title("Heatmap Korelasi antara Variabel")
st.pyplot(fig)

# Section 4: Tren Penggunaan Sepeda Berdasarkan Musim
st.subheader("Tren Penggunaan Sepeda Berdasarkan Musim")
seasonal_rentals = filtered_df.groupby("season_day")["cnt_day"].mean()

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=seasonal_rentals.index, y=seasonal_rentals.values, palette="viridis", ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata Peminjaman Sepeda")
ax.set_title("Rata-rata Peminjaman Sepeda Berdasarkan Musim")
st.pyplot(fig)

st.caption("Dashboard Analisis Bike Sharing | Data dari Proyek Bike Sharing")
