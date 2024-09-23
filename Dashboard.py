import streamlit as st
import pandas as pd
import plotly_express as px
import openpyxl

st.set_page_config(layout='wide')

with st.container(border=True):
    st.title(":green[Kecamatan di Jawa Barat Dalam Visualisasi Data]")
#st.subheader("", divider='rainbow')

st.subheader(":green[SUMBER DATA]")
with st.expander("Sumber Data"):
    st.success("Data yang ditampilkan diperoleh dari:")
    st.link_button("Open Data Jabar", url="https://opendata.jabarprov.go.id/id/dataset/jumlah-kepala-keluarga-berdasarkan-desakelurahan-di-jawa-barat")
    st.link_button("Portal Data Desa Jabar", url="https://portaldatadesa.jabarprov.go.id/")
    
st.subheader("", divider='rainbow')
