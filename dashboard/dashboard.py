import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import locale

# load berkas pada dataframe
df_final = pd.read_csv("Project_E-commers.csv")

# Konversi kolom order_purchase_timestamp ke format datetime
df_final["order_purchase_timestamp"] = pd.to_datetime(df_final["order_purchase_timestamp"])
# Melakukan pengurutan berdasarkan kolom order_purchase_timestamp
df_final.sort_values(by="order_purchase_timestamp", inplace=True)
# Reset index setelah pengurutan
df_final.reset_index(drop=True, inplace=True)


# Set locale menjadi en_US
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

#menampilkan total order dan total revenue
st.header('Brazilian E-Commerce')

col1, col2 = st.columns(2)
with col1:
    total_orders = df_final['order_item_id'].sum()
    st.metric("Total orders", value=total_orders)

with col2:
    total_revenue = df_final['price'].sum()
    # Konversi nilai pendapatan ke format USD
    formatted_revenue = locale.currency(total_revenue, grouping=True)
    st.metric("Total Revenue", value=formatted_revenue)

st.subheader("Tren Penjualan 2016-2018")
# Menghasilkan data dummy untuk contoh
dates = pd.date_range('2016-09-03', periods=616, freq='D')
values = df_final.groupby('order_purchase_timestamp')['price'].sum()

df = pd.DataFrame({'Date': dates, 'Value': values})

df.set_index('Date', inplace=True)

# Membuat gambar dan sumbu
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(
    df.index,  # Menggunakan indeks tanggal dari DataFrame
    df['Value'],  # Menggunakan nilai dari DataFrame
    marker='o',
    markersize=3,
    color='blue'
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

# Menampilkan plot di Streamlit
st.pyplot(fig)

#membuat bar chart
st.subheader("Total Order Per-state")

fig, ax = plt.subplots(figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]

total_sales_state = df_final['customer_state'].value_counts()
total_sales_state.plot(kind='bar', figsize=(10,6))
ax.set_ylabel("Total Order", fontsize=25)
ax.set_xlabel("State", fontsize=25)
ax.set_title("Total Order per-State", loc="center", fontsize=40)
ax.tick_params(axis='y', labelsize=25)
ax.tick_params(axis='x', labelsize=12)
 
st.pyplot(fig)


st.subheader("Persentase Penjualan Products")
# Sebelumnya telah membuat DataFrame df_counts
# Menghitung nilai yang berbeda dalam kolom 'product_category_name' dan simpan jumlahnya dalam df_counts
value_counts = df_final['product_category_name'].value_counts()
df_counts = pd.DataFrame(value_counts)
df_counts.columns = ['Total_penjualan_product']

# Reset indeks DataFrame untuk mengubah indeks menjadi kolom
df_counts.reset_index(inplace=True)

# Ubah nama kolom indeks menjadi 'product_category_name'
df_counts.rename(columns={'index': 'product_category_name'}, inplace=True)

# Tampilkan DataFrame yang dihasilkan
print(df_counts)

top_3_products = df_counts.nlargest(3, 'Total_penjualan_product')
total_others = df_counts['Total_penjualan_product'].sum() - top_3_products['Total_penjualan_product'].sum()
others = pd.DataFrame({'product_category_name': ['Others'], 'Total_penjualan_product': [total_others]})
df_combined = pd.concat([top_3_products, others])

# Visualisasikan data menggunakan pie chart
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(df_combined['Total_penjualan_product'], labels=df_combined['product_category_name'], autopct='%1.1f%%', startangle=140)
ax.set_title('Top 3 Products + Others')
ax.axis('equal')  # Memastikan pie chart berbentuk lingkaran

# Tampilkan plot di Streamlit
st.pyplot(fig)

st.caption('Copyright © Sukma Mulyani')