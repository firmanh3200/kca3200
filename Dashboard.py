import streamlit as st
import pandas as pd
import plotly_express as px
import openpyxl

st.set_page_config(layout='wide')

with st.container(border=True):
    st.title(":green[Bahan Grafik Kecamatan Dalam Angka]")
#st.subheader("", divider='rainbow')

st.subheader(":blue[LATAR BELAKANG]")
with st.expander("Latar Belakang"):
    st.info("Publikasi Kecamatan Dalam Angka harus dapat terbit tepat waktu dan berkualitas. \
        Keterbatasan sumber data, waktu dan tenaga penyusun publikasi sangat mempengaruhi \
        kualitas dari publikasi.")

st.subheader(":red[PERMASALAHAN]")
with st.expander("Permasalahan"):
    st.warning("Selama ini para penyusun publikasi Kecamatan Dalam Angka melakukan pengumpulan data \
        secara parsial, tanpa memperhatikan konsistensi dan kewajaran data antar wilayah. \
            Selain itu, para penyusun melakukan pembuatan grafik masing-masing, sehingga \
                waktu dan tenaga menjadi kurang efektif/ efisien.")

st.subheader(":green[SOLUSI ALTERNATIF]")
with st.expander("Solusi Alternatif"):
    st.success("Dashboard ini dibangun sebagai alternatif solusi sementara untuk mengefisienkan \
        waktu, dan mengefektifkan tenaga para penyusun publikasi Kecamatan Dalam Angka, sehingga mereka dapat \
            dengan mudah memilih jenis dan warna grafik dan mengunduhnya untuk dipasang \
                di publikasi masing-masing. Selain itu, tersedia pula tabel dan keterangan sumber data diperoleh.")

st.subheader(":green[TUJUAN]")
with st.expander("Tujuan"):
    st.success("Koordinasi dan Kerjasama antara BPS sebagai Pembina Data, Diskominfo sebagai Walidata, dan Dinas/ Badan/ Kantor/ \
        Kecamatan/ Kelurahan sebagai Produsen Data dalam Mewujudkan Satu Data Indonesia.")

st.subheader(":green[SUMBER DATA]")
with st.expander("Sumber Data"):
    st.success("Data yang ditampilkan diperoleh dari:")
    st.link_button("Open Data Jabar", url="https://opendata.jabarprov.go.id/id/dataset/jumlah-kepala-keluarga-berdasarkan-desakelurahan-di-jawa-barat")
    st.link_button("Portal Data Desa Jabar", url="https://portaldatadesa.jabarprov.go.id/")
    
st.subheader("", divider='rainbow')
