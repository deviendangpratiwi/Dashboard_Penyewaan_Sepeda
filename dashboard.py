import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
from babel.numbers import format_currency
sns.set(style='dark')


clean_day = pd.read_csv("clean_day.csv")
clean_hour = pd.read_csv("clean_hour.csv")

clean_day["dteday"] = pd.to_datetime(clean_day["dteday"])
clean_hour["dteday"] = pd.to_datetime(clean_hour["dteday"])

#Judul Dashboard
st.title("Dashboard Penyewaan Sepeda🚲")

# Sidebar
st.sidebar.image("icon.jpg", use_container_width=True)
st.sidebar.title("Rentang Waktu")

# Pilih Dataset
dataset = st.sidebar.selectbox("Pilih Dataset", ["Harian", "Per Jam"])

# Gunakan dataset yang dipilih
if dataset == "Harian":
    df = clean_day
else:
    df = clean_hour

min_date = clean_day["dteday"].min().date()  
max_date = clean_day["dteday"].max().date()  

start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)
filtered_df = clean_day[(clean_day["dteday"] >= start_date) & (clean_day["dteday"] <= end_date)]


# Filter data berdasarkan tanggal
filtered_df = clean_day[(clean_day["dteday"] >= start_date) & 
                         (clean_day["dteday"] <= end_date)]

col1, col2, col3 = st.columns(3)
if dataset == "Harian":
    col1.metric("Total Penyewaan Harian", filtered_df["cnt"].sum())
    col2.metric("Total Penyewa Terdaftar", filtered_df["registered"].sum())
    col3.metric("Total Penyewa Kasual", filtered_df["casual"].sum())
else:
    col1.metric("Rata-rata Penyewaan Harian", round(filtered_df["cnt"].mean(), 2))
    col2.metric("Rata-rata Penyewa Terdaftar", round(filtered_df["registered"].mean(), 2))
    col3.metric("Rata-rata Penyewa Kasual", round(filtered_df["casual"].mean(), 2))

st.subheader("📈 Penyewaan Sepeda dalam Tahun 2011 dan 2012")

fig = px.line(filtered_df, x="dteday", y="cnt", title="Tren Penyewaan Sepeda Harian")
fig.update_layout(
    xaxis_title="Tanggal",
    yaxis_title="Jumlah Penyewaan Sepeda")
st.plotly_chart(fig)
with st.expander("Lihat Penjelasan"):
    st.write("Penyewaan sepeda meningkat secara bertahap dari awal tahun hingga pertengahan tahun dan mencapai puncaknya sekitar pertengahan hingga akhir tahun 2012 sebelum mulai menurun. Tren ini mengindikasikan adanya pola musiman, di mana mungkin jumlah penyewaan meningkat saat cuaca atau musim lebih mendukung dan menurun saat cuaca atau musim kurang bersahabat.")

#Visualisasi Perbandingan Penyewaan Sepeda antara Hari Kerja & Akhir Pekan
st.subheader("Perbandingan Penyewaan Sepeda: Hari Kerja vs Akhir Pekan")
fig, ax = plt.subplots(figsize=(6, 5))
sns.barplot(
    x="workingday", y="cnt", data=clean_day, estimator="mean",
    errorbar=None, palette=["lightblue", "darkblue"], hue="workingday", legend=False)
ax.set_xticks([0, 1])
ax.set_xticklabels(["Akhir Pekan", "Hari Kerja"])
ax.set_xlabel("Kategori Hari")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
st.pyplot(fig)
with st.expander("Lihat Penjelasan & Strategi"):
    st.write("Dari grafik batang, terlihat bahwa rata-rata penyewaan sepeda lebih tinggi pada **hari kerja** dibandingkan **akhir pekan**. Ini menunjukkan bahwa banyak pengguna sepeda menggunakan layanan ini untuk kebutuhan transportasi harian seperti pergi ke kantor atau sekolah.")
    st.write("📌 **Strategi Harga & Promosi:**")
    st.markdown("""
    - **Hari kerja:** Bisa diterapkan **paket langganan mingguan/bulanan** dengan harga yang lebih murah untuk menarik pelanggan tetap.
    - **Akhir pekan:** Bisa dibuat promosi seperti **diskon atau program sewa satu jam gratis** untuk menarik pelanggan rekreasi.""")

# Rata-rata penyewaan sepeda per musim
st.subheader("Proporsi Rata-rata Penyewaan Sepeda Berdasarkan Musim")
season_avg = clean_day.groupby("season", as_index=False)["cnt"].mean()
colors = ['#87CEFA','#00008B', '#4682B4','#ADD8E6']
fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(season_avg["cnt"], labels=season_avg["season"], autopct="%1.1f%%", colors=colors, startangle=140)
st.pyplot(fig)
with st.expander("Lihat Penjelasan & Strategi"):
    st.write("Dari pie chart, penyewaan sepeda paling tinggi terjadi pada **musim gugur (31.4%)**, diikuti oleh **musim panas (27.8%)** dan **musim dingin (26.3%)**. Penyewaan paling rendah terjadi di **musim semi (14.5%)**. Semakin pekat warna pie chart, semakin tinggi proporsi penyewaan. Hal ini menunjukkan bahwa pengguna lebih sering menyewa sepeda saat cuaca lebih nyaman.")
    st.write("📌 **Strategi Harga & Promosi:**")
    st.markdown("""
    - **Musim gugur & panas:** Harga bisa lebih tinggi karena permintaan tinggi.
    - **Musim dingin & semi:** Bisa diberikan diskon untuk menarik lebih banyak pengguna, misalnya paket sewa khusus musim dingin.""")

#Boxplot jumlah penyewaan berdasarkan cuaca
st.subheader("Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
colors = ['#4682B4', '#00008B', '#ADD8E6']
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(x='weathersit', y='cnt', data=clean_day, hue="weathersit", palette=colors, legend=False, ax=ax)
ax.set_xlabel("Cuaca")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)
with st.expander("Lihat Penjelasan & Strategi"):
    st.write("Dari boxplot cuaca, terlihat bahwa penyewaan sepeda paling tinggi saat **cuaca cerah**, menurun saat **mendung**, dan paling rendah saat **hujan**. Ini menunjukkan bahwa kondisi cuaca sangat mempengaruhi minat pelanggan dalam menyewa sepeda.")
    st.write("📌 **Strategi Harga & Promosi:**")
    st.markdown("""
    - **Cuaca cerah:** Bisa menerapkan **harga normal** atau **promosi** untuk menarik lebih banyak penyewa.
    - **Cuaca mendung:** Bisa memberikan **diskon** agar tetap ada penyewa meskipun langit mendung.
    - **Cuaca hujan:** Bisa menawarkan **diskon besar** atau **paket khusus indoor** (misalnya diskon untuk pelanggan yang menyewa di hari hujan).""")
st.subheader("🔍 Insight")
st.markdown("""
- **Penyewaan sepeda lebih tinggi pada hari kerja** untuk kebutuhan transportasi harian, sedangkan lebih rendah di akhir pekan. Terapkan **paket langganan** untuk hari kerja dan **diskon** di akhir pekan.
- **Penyewaan tertinggi terjadi di musim gugur & panas**, sementara terendah di musim semi. Kenakan **harga premium** di musim gugur & panas, dan beri **diskon di musim semi atau dingin**.
- **Cuaca cerah meningkatkan penyewaan**, sementara mendung dan hujan menurunkan minat. Terapkan **harga normal di cuaca cerah**, dan tawarkan **diskon saat mendung atau hujan**.""")

#Heatmap Penyewaan Sepeda berdasarkan hari dan jam
st.subheader("Heatmap Penyewaan Sepeda berdasarkan hari dan jam")
day_mapping = {'Minggu': 0, 'Senin': 1, 'Selasa': 2, 'Rabu': 3,
               'Kamis': 4, 'Jumat': 5, 'Sabtu': 6}
clean_hour['weekday'] = clean_hour['weekday'].map(day_mapping).fillna(clean_hour['weekday']).astype(int)
day_labels = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
clean_hour['weekday'] = clean_hour['weekday'].map(dict(enumerate(day_labels)))
pivot_table = clean_hour.pivot_table(values="cnt", index="weekday", columns="hr", aggfunc="mean")
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(pivot_table, cmap="coolwarm", annot=True, fmt=".0f", linewidths=0.5, ax=ax)
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Hari dalam Seminggu")
st.pyplot(fig)
with st.expander("Lihat Penjelasan"):
    st.write("Pada hari kerja (Senin - Jumat), penyewaan meningkat pada pukul 07:00 - 09:00 dan 17:00 - 19:00, sehingga perlu disiapkan lebih banyak sepeda pada jam-jam tersebut, sementara pada jam sepi cukup dialokasikan stok minimal. Akhir pekan menunjukkan lonjakan lebih merata sepanjang hari, terutama dari pagi hingga sore, sehingga stok sepeda perlu ditingkatkan pada rentang waktu tersebut. Untuk menghindari kekurangan atau kelebihan stok, penggunaan sistem pemantauan real-time dan redistribusi sepeda secara dinamis akan membantu memastikan ketersediaan sepeda tetap optimal di berbagai lokasi.")
st.subheader("🔍 Insight")
st.markdown("""
- **Memastikan stok sepeda cukup tinggi pada jam sibuk (07:00 - 09:00 & 17:00 - 19:00)** untuk mengakomodasi lonjakan pengguna. Redistribusi sepeda dari area dengan permintaan rendah ke area dengan permintaan tinggi sebelum jam sibuk dimulai.  
- **Penyewaan lebih merata sepanjang hari di akhir pekan**, dengan peningkatan signifikan dari siang hingga sore. Sebarkan stok lebih merata dan terapkan sistem pemesanan online atau pre-booking untuk menghindari kekurangan saat jam ramai.""")

#Hubungan suhu, kelembaban dan windspeed vs penyewaan sepeda
st.subheader("Matriks Korelasi Faktor Cuaca dan Penyewaan Sepeda")
corr_matrix = clean_day[['temp', 'hum', 'windspeed', 'cnt']].corr()
fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
st.pyplot(fig)
st.subheader("Plot Hubungan Faktor Cuaca dengan Penyewaan Sepeda")
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
sns.regplot(x='temp', y='cnt', data=clean_day, ax=axes[0], scatter_kws={'alpha':0.5})
axes[0].set_title("Hubungan Suhu vs Penyewaan Sepeda")
sns.regplot(x='hum', y='cnt', data=clean_day, ax=axes[1], scatter_kws={'alpha':0.5})
axes[1].set_title("Hubungan Kelembaban vs Penyewaan Sepeda")
sns.regplot(x='windspeed', y='cnt', data=clean_day, ax=axes[2], scatter_kws={'alpha':0.5})
axes[2].set_title("Hubungan Kecepatan Angin vs Penyewaan Sepeda")
plt.tight_layout()
st.pyplot(fig)
st.subheader("🔍 Insight")
st.markdown("""
- **Suhu berpengaruh positif** terhadap penyewaan sepeda (**r = 0.63**), semakin hangat, semakin banyak penyewa.  
- **Kelembaban memiliki pengaruh lemah** (**r = -0.10**), artinya tidak terlalu memengaruhi keputusan menyewa.  
- **Kecepatan angin berpengaruh negatif** (**r = -0.23**), angin kencang cenderung menurunkan minat bersepeda.  
- **Faktor cuaca berpengaruh**, tetapi ada faktor lain seperti hari kerja, akhir pekan, atau jam sibuk yang lebih dominan.
""")

#Rata-rata Penyewaan Sepeda per Bulan (Dibandingkan antara 2011 & 2012)
st.subheader("Rata-rata Penyewaan Sepeda per Bulan (Dibandingkan antara 2011 & 2012)")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(
    x="mnth", y="cnt", hue="yr", data=clean_day,
    estimator="mean", errorbar=None, marker="o", palette=["blue", "red"], ax=ax)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agt", "Sep", "Okt", "Nov", "Des"])
ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.legend(title="Tahun", labels=["2011", "2012"])
ax.grid(True)
st.pyplot(fig)
st.subheader("🔍 Insight")
st.markdown("""
- **Terdapat pola musiman**, penyewaan meningkat pada pertengahan tahun (Mei-September) dan menurun di awal serta akhir tahun. Strategi: Tambah stok sepeda saat musim ramai dan kurangi saat permintaan rendah.
- **Tahun 2012 lebih tinggi dibanding 2011** di hampir setiap bulan. Kemungkinan faktor: Pertumbuhan pengguna, peningkatan fasilitas, atau promosi.
- Jika ingin **mengalokasikan sepeda secara optimal**, stok harus ditingkatkan di pertengahan tahun dan dikurangi di bulan-bulan dengan permintaan rendah.""")

# Penyewaan Sepeda oleh Pelanggan Terdaftar vs Kasual
st.subheader("Pola Penyewaan Sepeda oleh Pelanggan Terdaftar vs. Kasual")
fig, ax = plt.subplots(figsize=(10, 5))
day_grouped = clean_day.groupby("weekday")[["registered", "casual"]].mean()
day_grouped.plot(kind="bar", ax=ax, color=["#1E40AF", "#93C5FD"])
ax.set_xticks(range(7))
ax.set_xticklabels(["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"], rotation=0)
ax.set_xlabel("Hari dalam Seminggu")
ax.set_ylabel("Rata-rata Penyewaan")
ax.legend(["Terdaftar", "Kasual"])
ax.grid(axis="y", linestyle="--", alpha=0.7)
st.pyplot(fig)
# Insight
st.subheader("🔍 Insight")
st.markdown("""
- **Pelanggan Terdaftar**: Penyewaan stabil & lebih tinggi saat hari kerja → optimalkan sepeda di jam kerja.
- **Pelanggan Kasual**: Menambah promosi & perbanyak sepeda di area wisata.
""")

#Analisis Lanjutan
def kategori_penyewaan(cnt):
    if cnt < 1000:
        return "Rendah ( <1000 )"
    elif 1000 <= cnt < 2500:
        return "Sedang (1000 - 2499)"
    elif 2500 <= cnt < 4000:
        return "Tinggi (2500 - 3999)"
    else:
        return "Sangat Tinggi (≥4000)"
clean_day = pd.read_csv("clean_day.csv")
clean_day["Kategori_Penyewaan"] = clean_day["cnt"].apply(kategori_penyewaan)
st.subheader("Distribusi Kategori Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(10, 6))
clean_day["Kategori_Penyewaan"].value_counts().sort_index().plot(
    kind="barh", color=["#A9C9FF", "#1D4ED8", "#77A6F7", "#4C6EF5"], ax=ax)
ax.set_xlabel("Jumlah Hari")
ax.set_ylabel("Kategori Penyewaan")
plt.grid(axis="x", linestyle="--", alpha=0.7)
st.pyplot(fig)
st.subheader("🔍 Insight")
st.markdown(
    """
    - **Mayoritas hari memiliki jumlah penyewaan sangat tinggi (≥4000).** Ini menunjukkan permintaan sepeda stabil dan tinggi.
    - **Fluktuasi terlihat pada kategori sedang (1000-2499) dan tinggi (2500-3999).** Perlu strategi redistribusi stok agar seimbang.
    - **Hari dengan penyewaan rendah (<1000) sangat sedikit.** Bisa diterapkan promosi untuk meningkatkan pemakaian di hari-hari ini.
    """
)