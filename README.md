## Setup Environment - Shell/Terminal

```
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run steamlit app

```
cd dashboard
streamlit run dashboard.py
```

## Cara Menjalankan dashboard

```
    sidebar
        pilih halaman, berfungsi untuk memilih halaman yang akan ditampilkan di layar(pilih opsi yang diinginkan).
        filter, terdapat berbagai macam filter berfungsi untuk memfilter data yang akan ditampilkan (default kosong)

    halaman:
    Seluruh halaman dapat digabungkan oleh menu filter di dalam sidebar.

        halaman home, berfungsi untuk menampilkan data berbentuk tabel.
            cara penggunaan:
                1. tekan "pilih kolom", jika sudah akan muncul tampilan.
                2. tekan "choose an option" untuk memilih kolom yang ingin anda tampilkan

        halaman Transaksi, berfungsi untuk melihat frekuensi dan total transaksi dari tahun ke tahun.
            cara penggunaan:
                pilih opsi yang ingin ditampilkan total transaksi/Total_keuntungan

        halaman barChart, berfungsi untuk membandingkan frekuensi dan total transaksi dari beberapa data
            cara penggunaan:
                1. pilih opsi sumbu y yang diinginkan.
                2. pilih opsi sumbu x yang diinginkan.
                3. pilih opsi sorting yang diinginkan mau menaik atau menurun.


```
