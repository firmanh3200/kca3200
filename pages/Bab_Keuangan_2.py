import streamlit as st
import pandas as pd
import plotly_express as px
import openpyxl

st.set_page_config(layout='wide')

st.title(":green[Grafik Kecamatan Dalam Angka]")

st.header(":blue[BAB KEUANGAN - KOPERASI]")
st.subheader("", divider='rainbow')
#with st.expander("KETERANGAN"):
#    st.write("pad = Pendapatan Asli Desa")
#    st.write("dd = Dana Desa")
#    st.write("pajak_dan_retribusi = Bagi Hasil Pajak dan Retribusi")
#    st.write("alokasi_dd = Alokasi Dana Desa")
#    st.write("bantuan_prov = Bantuan Pemerintah Provinsi")
#    st.write("bantuan_kabkot = Bantuan Pemerintah Kabupaten/ Kota")
#    st.write("lainnya = Sumber Pendapatan Lainnya")

datakk = pd.read_excel("data/koperasi_desa.xlsx")
sort_datakk = datakk.sort_values(by=['tahun', 'namakab', 'namakec', 'namadesa'], ascending=[False,True,True,True])
#sort_datakk = sort_datakk.groupby(['namakab', 'namakec', 'namadesa','tahun'])[['jumlah_gurusd', 'jumlah_gurusmp', 'jumlah_gurusma']].sum().reset_index()

pilihankab = sort_datakk['namakab'].unique()

pilihantahun = sort_datakk['tahun'].unique()

#pilihanjenjang = ['pad', 'dd', 'pajak_dan_retribusi', 'alokasi_dd', 'bantuan_prov', 'bantuan_kabkot', 'lainnya']

# Pilihan tema warna
warna_options = {
    'Viridis': px.colors.sequential.Viridis,
    'Pastel2': px.colors.qualitative.Pastel2,
    'Greens': px.colors.sequential.Greens,
    'Inferno': px.colors.sequential.Inferno,
    'Set1': px.colors.qualitative.Set1,
    'Set2': px.colors.qualitative.Set2,
    'Set3': px.colors.qualitative.Set3,
    'Pastel1': px.colors.qualitative.Pastel1,
    'Blues': px.colors.sequential.Blues,
    'Reds': px.colors.sequential.Reds,
    'YlGnBu': px.colors.sequential.YlGnBu,
    'YlOrRd': px.colors.sequential.YlOrRd,
    'RdBu': px.colors.diverging.RdBu,
    'Spectral': px.colors.diverging.Spectral
}

kol1a, kol1b, kol1d, kol1e = st.columns(4)
with kol1a:
    pilihkab = st.selectbox("Filter Kab/Kota", pilihankab, key='kab1')
with kol1b:
    pilihankec = sort_datakk[sort_datakk['namakab'] == pilihkab]['namakec'].unique()
    pilihkec = st.selectbox("Filter Kecamatan", pilihankec, key='kec1')
#with kol1c:
#    dataterpilih = st.selectbox("Filter Jenis Pendapatan Desa", pilihanjenjang, key='tahun2')
with kol1d:
    pilihtahun = st.selectbox("Pilih Tahun Data:", pilihantahun, key='tahun1')
with kol1e:
    pilihwarna = st.selectbox("Pilih Tema Warna:", options=list(warna_options.keys()))

# JUMLAH KK
with st.container(border=True):
    st.info(f"Jumlah Koperasi Aktif di Kecamatan {pilihkec}, {pilihkab} Tahun {pilihtahun}")
    kol1d, kol1e, kol1f = st.columns(3)
    if pilihkab and pilihkec:
        tabelkk = sort_datakk[(sort_datakk['namakab'] == pilihkab) & (sort_datakk['namakec'] == pilihkec) & (sort_datakk['tahun'] == pilihtahun)].sort_values(by='koperasi_aktif', ascending=False)
        #tabelkk2 = tabelkk[['namakec', 'jumlah_sd', 'jumlah_smp', 'jumlah_sma']]
        
        with kol1d:
            pie_kk = px.pie(tabelkk, values='koperasi_aktif', names='namadesa', 
                            color_discrete_sequence=warna_options[pilihwarna])
            pie_kk.update_layout(
                    legend=dict(
                        orientation="h",  # Horizontal orientation
                        yanchor="top",    # Anchor the legend to the top
                        y=-0.2,           # Position the legend below the chart
                        xanchor="center",  # Center the legend horizontally
                        x=0.5              # Center the legend at the middle of the chart
                    )
                )
            with st.container(border=True):
                st.plotly_chart(pie_kk, use_container_width=True)
        with kol1e:
            bar_kk = px.bar(tabelkk, x='namadesa', y='koperasi_aktif', color='namadesa',
                            text='koperasi_aktif',            
                            color_discrete_sequence=warna_options[pilihwarna])
            bar_kk.update_layout(showlegend=False)
            with st.container(border=True):
                st.plotly_chart(bar_kk, use_container_width=True)
        with kol1f:
            bar_kk2 = px.bar(tabelkk, x='koperasi_aktif', y='namadesa', color='namadesa',
                            text='koperasi_aktif', orientation='h',            
                            color_discrete_sequence=warna_options[pilihwarna])
            bar_kk2.update_layout(showlegend=False)
            with st.container(border=True):
                st.plotly_chart(bar_kk2, use_container_width=True)

st.subheader("", divider='rainbow')
with st.container(border=True):
    st.info(f"Jumlah Koperasi Aktif di Kecamatan {pilihkec}, {pilihkab} Tahun {pilihtahun}")
    kol2a, kol2b = st.columns(2)
    trimep = px.treemap(tabelkk, path=['namakec', 'namadesa'], values='koperasi_aktif', 
                        color_discrete_sequence=warna_options[pilihwarna])
    trimep.update_traces(textinfo='label+value')
    
    sunburst = px.sunburst(tabelkk, path=['namakec', 'namadesa'], values='koperasi_aktif', 
                        color_discrete_sequence=warna_options[pilihwarna])
    sunburst.update_traces(textinfo='label+value')
    
    with kol2a:
        with st.container(border=True):
            st.plotly_chart(trimep, use_container_width=True)
    
    with kol2b:
        with st.container(border=True):
            st.plotly_chart(sunburst, use_container_width=True)

st.subheader("", divider='rainbow')
        
with st.container(border=True):
    tabelseri = datakk[(datakk['namakab'] == pilihkab) & (datakk['namakec'] == pilihkec)]
    tabelseri = tabelseri[['tahun', 'namakab', 'namakec', 'namadesa', 'koperasi_aktif']]
    tabelseri = tabelseri.sort_values(by=['tahun', 'namakec', 'namadesa'], ascending=[False, True, True])
    st.dataframe(tabelseri, use_container_width=True, hide_index=True)

st.subheader("", divider='rainbow')
    
st.link_button("sumber Data", url="https://portaldatadesa.jabarprov.go.id/index-profile-desa/Ekonomi")
