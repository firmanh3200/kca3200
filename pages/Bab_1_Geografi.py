import streamlit as st
import pandas as pd
import plotly_express as px
import openpyxl

st.set_page_config(layout='wide')

st.title(":green[Grafik Kecamatan Dalam Angka]")

st.header(":blue[BAB 1 GEOGRAFI]")
st.subheader("", divider='rainbow')

datakk = pd.read_excel("data/geografi_desa.xlsx")
sort_datakk = datakk.sort_values(by=['tahun', 'namakab', 'namakec', 'namadesa'], ascending=[False,False,True,True])

pilihankab = sort_datakk['namakab'].unique()

pilihantahun = sort_datakk['tahun'].unique()


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

kol1a, kol1b, kol1c, kol1d = st.columns(4)
with kol1a:
    pilihkab = st.selectbox("Filter Kab/Kota", pilihankab, key='kab1')
with kol1b:
    pilihankec = sort_datakk[sort_datakk['namakab'] == pilihkab]['namakec'].unique()
    pilihkec = st.selectbox("Filter Kecamatan", pilihankec, key='kec1')
with kol1c:
    pilihtahun = st.selectbox("Filter Tahun", pilihantahun, key='tahun1')
with kol1d:
    pilihwarna = st.selectbox("Pilih Tema Warna:", options=list(warna_options.keys()))

# JUMLAH KK
with st.container(border=True):
    st.info(f"Luas Wilayah Desa di Kecamatan {pilihkec}, {pilihkab} Tahun {pilihtahun} (Km2)")
    kol1d, kol1e, kol1f = st.columns(3)
    if pilihkab and pilihkec and pilihtahun:
        tabelkk = datakk[(datakk['namakab'] == pilihkab) & (datakk['namakec'] == pilihkec) & (datakk['tahun'] == pilihtahun)]
        tabelkk2 = tabelkk[['namadesa', 'luas_desa']].sort_values(by='luas_desa', ascending=False)
        
        with kol1d:
            pie_kk = px.pie(tabelkk2, values='luas_desa', names='namadesa', 
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
            bar_kk = px.bar(tabelkk2, x='namadesa', y='luas_desa', color='namadesa',
                            text='luas_desa',            
                            color_discrete_sequence=warna_options[pilihwarna])
            bar_kk.update_layout(showlegend=False)
            with st.container(border=True):
                st.plotly_chart(bar_kk, use_container_width=True)
        with kol1f:
            bar_kk2 = px.bar(tabelkk2, x='luas_desa', y='namadesa', color='namadesa',
                            text='luas_desa', orientation='h',
                            color_discrete_sequence=warna_options[pilihwarna])
            bar_kk2.update_layout(showlegend=False)
            with st.container(border=True):
                st.plotly_chart(bar_kk2, use_container_width=True)

st.subheader("", divider='rainbow')
with st.container(border=True):
    st.info(f"Luas Wilayah di Kecamatan {pilihkec}, {pilihkab} Tahun {pilihtahun} (Km2)")
    kol2a, kol2b = st.columns(2)
    trimep = px.treemap(tabelkk, path=['namakec', 'namadesa'], values='luas_desa', 
                        color_discrete_sequence=warna_options[pilihwarna])
    trimep.update_traces(textinfo='label+value')
    
    sunburst = px.sunburst(tabelkk, path=['namakec', 'namadesa'], values='luas_desa', 
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
    tabelkk3 = datakk[(datakk['namakab'] == pilihkab) & (datakk['namakec'] == pilihkec)]
    st.dataframe(tabelkk3, hide_index=True, use_container_width=True)
st.subheader("", divider='rainbow')
    
st.link_button("sumber Data", url="https://portaldatadesa.jabarprov.go.id/index-profile-desa/Lingkungan/Geografi")
