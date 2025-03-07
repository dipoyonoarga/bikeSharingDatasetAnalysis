# Import library
import matplotlib.dates as mdates
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset day
day = pd.read_csv("data/day.csv")

# Mengubah tipe data
day["dteday"] = pd.to_datetime(day["dteday"])

# Mengatur rentang tanggal yang valid untuk filter
start_date = pd.to_datetime("2011-01-01")
end_date = pd.to_datetime("2012-12-31")

# Sidebar untuk memilih periode tanggal
st.sidebar.title("Pilih Periode Tanggal")
start_date_input = st.sidebar.date_input("Tanggal Mulai", start_date)
end_date_input = st.sidebar.date_input("Tanggal Akhir", end_date)

# Memastikan tanggal yang dipilih tidak melampaui rentang dataset
if start_date_input > end_date_input:
    st.sidebar.error(
        "Tanggal mulai tidak bisa lebih besar dari tanggal akhir.")
else:
    st.sidebar.write(
        f"Menampilkan data antara: {start_date_input} dan {end_date_input}")

# Mengonversi tanggal yang dipilih ke format datetime
start_date_input = pd.to_datetime(start_date_input)
end_date_input = pd.to_datetime(end_date_input)

# Memfilter data berdasarkan rentang tanggal yang dipilih
filtered_data = day[(day['dteday'] >= start_date_input)
                    & (day['dteday'] <= end_date_input)]

# Mapping kondisi cuaca
weatherMap = {
    1: "Cerah/Sedikit Berawan",
    2: "Kabut/Berawan",
    3: "Sedikit Hujan/Bersalju"
}

filtered_data["weathersit"] = filtered_data["weathersit"].map(weatherMap)

# Fungsi untuk visualisasi


def weatherImpact():
    weather_df = filtered_data.groupby(by="weathersit").cnt.sum().reset_index()
    weather_df.rename(columns={
        "weathersit": "kondisi_cuaca",
        "cnt": "jumlah_sepeda"
    }, inplace=True)

    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3"]

    fig, ax = plt.subplots(figsize=(8, 6))
    barChart = sns.barplot(
        x="kondisi_cuaca",
        y="jumlah_sepeda",
        data=weather_df.sort_values(by="jumlah_sepeda", ascending=False),
        palette=colors,
        ax=ax
    )

    for bar in barChart.patches:
        barChart.annotate(f'{bar.get_height():,.0f}',
                          (bar.get_x() + bar.get_width() / 2., bar.get_height()),
                          ha='center', va='bottom', fontsize=12, color='black')

    ax.set_ylim(0, max(weather_df["jumlah_sepeda"]) * 1.1)
    ax.set_title("Jumlah Sepeda yang Dipinjam Berdasarkan Kondisi Cuaca",
                 loc="center", fontsize=15)
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Jumlah Sepeda")

    st.pyplot(fig)


def tempImpact():
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(
        x="temp",
        y="cnt",
        data=filtered_data,
        alpha=0.6,
        palette="Set1",
        ax=ax
    )
    ax.set_title("Hubungan antara Suhu dengan Jumlah Sepeda yang Dipinjam")
    ax.set_xlabel("Suhu")
    ax.set_ylabel("Jumlah Sepeda")

    st.pyplot(fig)


def monthlyTrend():
    monthly = filtered_data.groupby(filtered_data["dteday"].dt.to_period("M"))[
        "cnt"].sum().reset_index()
    monthly["dteday"] = monthly["dteday"].astype(str)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(
        monthly["dteday"],
        monthly["cnt"],
        marker='o',
        linewidth=2,
        color="#72BCD4"
    )
    ax.set_title("Tren Jumlah Sepeda yang Dipinjam", loc="center", fontsize=20)
    ax.set_xlabel("Bulan", fontsize=12)
    ax.set_ylabel("Jumlah Sepeda", fontsize=12)
    ax.set_xticklabels(monthly["dteday"], rotation=45, fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    st.pyplot(fig)


def binningClustering():
    bins = [0, 3000, 6000, np.inf]
    labels = ['Rendah', 'Sedang', 'Tinggi']
    filtered_data['category'] = pd.cut(filtered_data['cnt'], bins=bins,
                                       labels=labels, include_lowest=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(x=filtered_data['category'], palette='pastel', ax=ax)
    ax.set_title("Distribusi Kategori Penyewaan Sepeda")
    ax.set_xlabel("Kategori Penyewaan")
    ax.set_ylabel("Jumlah Hari")
    st.pyplot(fig)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.scatterplot(x=filtered_data['dteday'], y=filtered_data['cnt'],
                    hue=filtered_data['category'], palette='coolwarm', alpha=0.7, ax=ax)
    ax.set_title("Tren Penyewaan Sepeda dengan Kategori Binning")
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Sepeda")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.legend(title="Kategori Penyewaan")
    plt.xticks(rotation=45)
    st.pyplot(fig)


# Streamlit app layout
st.title('Dashboard Analisis Data Bike Sharing')
st.markdown("<br>", unsafe_allow_html=True)

st.subheader('Pengaruh Kondisi Cuaca Terhadap Jumlah Sepeda yang Dipinjam')
weatherImpact()
st.markdown("<br>", unsafe_allow_html=True)


st.subheader('Hubungan antara Suhu dengan Jumlah Sepeda yang Dipinjam')
tempImpact()
st.markdown("<br>", unsafe_allow_html=True)

st.subheader('Perkembangan Tren Jumlah Sepeda yang Dipinjam')
monthlyTrend()
st.markdown("<br>", unsafe_allow_html=True)

st.subheader('Pengelompokan Berdasarkan Tingkat Peminjaman Sepeda')
binningClustering()
st.markdown("<br>", unsafe_allow_html=True)
