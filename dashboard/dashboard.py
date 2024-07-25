import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

main_data_df = pd.read_csv(f'main_data.csv', delimiter=',')

st.set_page_config(page_title='Dashboard', layout='wide')

# Fungsi filter
def filter():
    filter_df = main_data_df
    # Sub-fungsi
    def status_order():
        filter_status= filter_df
        status= st.sidebar.selectbox(
        label='Pilih status_order',
        options= filter_status['order_status'].unique()
        )
        filter_status= filter_status.query('order_status == @status')
        return filter_status
    check_status= st.sidebar.checkbox(label= '&emsp; filter status order')
    if check_status: filter_df= status_order()
    
    def filter_negara():
        filter_negara = filter_df
        negara= st.sidebar.multiselect(
            'Pilih Negara',
            options= filter_negara['customer_state'].unique() if check_negara else [],
            default= []
        )
        filter_negara = filter_negara[filter_negara['customer_state'].isin(negara)]
        def filter_kota():
            filter_kota = filter_negara
            kota= st.sidebar.multiselect(
                'Pilih Kota',
                options= filter_kota['customer_city'].unique(),
                default= []
            )
            filter_kota = filter_kota[filter_kota['customer_city'].isin(kota)]
            filter_kota= filter_kota.query('customer_city == @kota')
            return filter_kota
        
        filter_negara= filter_negara.query('customer_state == @negara')
        check_kota = st.sidebar.checkbox(label= '&emsp; filter kota')
        if check_kota: filter_negara = filter_kota()
        return filter_negara
        filter_ 
    check_negara= st.sidebar.checkbox(label= '&emsp; filter negara')
    if check_negara: filter_df= filter_negara()
    
    def filter_produk():
        filter_produk = filter_df
        Produk= st.sidebar.multiselect(
        'Pilih Kategori Produk',
        options= filter_produk['product_category_name_english'].unique(),
        default= []
        )
        filter_produk= filter_produk.query('product_category_name_english == @Produk')
        return filter_produk
    check_produk= st.sidebar.checkbox(label= '&emsp; filter produk')
    if check_produk: filter_df= filter_produk()
    # ----------------
    return filter_df
# Fungsi halaman utama
def Home(): 
    with st.expander('Pilih Kolom'):
        showData= st.multiselect('Filter: ', main_data_df.columns, default=[])
        st.write(filter_df[showData])
# Fungsi untuk halaman kedua
def Halaman_pendapatan():
    pendapatan = filter_df
    pendapatan['order_delivered_customer_date'] = pd.to_datetime(pendapatan['order_delivered_customer_date'], errors='coerce', format='ISO8601')
    pendapatan = pendapatan.resample(rule='ME', on='order_delivered_customer_date').agg({
        'order_id': 'nunique',
        'price': 'sum'
    })
    pendapatan.index = pendapatan.index.strftime('%Y-%m') #mengubah format order date menjadi Tahun-Bulan
    pendapatan = pendapatan.reset_index()
    pendapatan.rename(columns={
        'order_delivered_customer_date': 'Tahun_Bulan',
        'order_id': 'Total Transaksi', 
        'price': 'Total_Keuntungan'
    }, inplace=True)
    st.title('Halaman Transaksi')
    y = st.selectbox(label='Pilih Opsi: ', options=['Total Transaksi', 'Total_Keuntungan'])
    fig, ax= plt.subplots(figsize=(10, 5))
    ax.yaxis.set_major_formatter(lambda x, _: f'{x:,.0f}')
    plt.plot(
        pendapatan['Tahun_Bulan'],
        pendapatan[y],
        marker='o', 
        linewidth=2,
        color='#72BCD4'
    )
    plt.xticks(fontsize=10, rotation= -45)
    plt.yticks(fontsize=10)
    st.pyplot(fig)
# Fungsi untuk halaman ketiga
def barChart():
    bar_df= filter_df 
    st.title('Halaman Ketiga')
    y = st.selectbox(label='Pilih Opsi Sumbu Y', options=['customer_state', 'customer_city', 'customer_unique_id', 'seller_id', 'product_category_name_english'])
    x = st.selectbox(label='Pilih Opsi Sumbu X', options=['price', 'order_id'])
    sort_val = st.selectbox(label='Pilih Opsi Sorting', options=['Terbesar', 'Terkecil'])
    val_sort = False if sort_val == 'Terbesar' else True
    if x == 'price':
        bar_df= bar_df.groupby(by= y)[x].sum().reset_index(name='Total')
    elif x == 'order_id':
        bar_df= bar_df.groupby(by= y)[x].count().reset_index(name='Total')
    bar_df= bar_df.sort_values(by= 'Total', ascending= val_sort).head(10)
    format_currency= "Rp" if x == 'price' else ""
    total = bar_df['Total']
    # plot
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.barh(bar_df[y],
            bar_df['Total'], 
            edgecolor='white', linewidth=0.7)
    for i in range(len(bar_df)):
        ax.text(bar_df['Total'].iloc[i], i, f'{format_currency} {int(total.iloc[i]):,}', va='center')
    ax.set_xlim(0, max(bar_df['Total']) * 1.15)
    ax.xaxis.set_major_formatter(lambda x, _: f'{x:,.0f}')
    ax.invert_yaxis()
    st.pyplot(fig)
    st.dataframe(bar_df)
# Pilihan halaman
pages = {
    'Home': Home,
    'Transaksi': Halaman_pendapatan,
    'barChart': barChart
}
# sidebar
st.sidebar.title('Menu Navigasi')
selection = st.sidebar.selectbox(label='Pilih Halaman:', options=list(pages.keys()))
page = pages[selection]
st.sidebar.header('Filter')
filter_df = filter()


page()
