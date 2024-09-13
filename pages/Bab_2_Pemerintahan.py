import streamlit as st
import pandas as pd
import plotly_express as px
import openpyxl

st.set_page_config(layout='wide')

st.title(":green[Grafik Kecamatan Dalam Angka]")

st.header(":blue[BAB 2 PEMERINTAHAN]")
st.subheader("", divider='rainbow')

datakk = pd.read_excel("data/jumlahrt.xlsx")
sort_datakk = datakk.sort_values(by=['nmkab', 'nmkec', 'nmdesa'], ascending=True)

pilihankab = sort_datakk['nmkab'].unique()

#pilihantahun = sort_datakk['tahun'].unique()


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

kol1a, kol1b, kol1d = st.columns(3)
with kol1a:
    pilihkab = st.selectbox("Filter Kab/Kota", pilihankab, key='kab1')
with kol1b:
    pilihankec = sort_datakk[sort_datakk['nmkab'] == pilihkab]['nmkec'].unique()
    pilihkec = st.selectbox("Filter Kecamatan", pilihankec, key='kec1')
#with kol1c:
#    pilihtahun = st.selectbox("Filter Tahun", pilihantahun, key='tahun1')
with kol1d:
    pilihwarna = st.selectbox("Pilih Tema Warna:", options=list(warna_options.keys()))

# JUMLAH KK
with st.container(border=True):
    st.info(f"Jumlah RT dan RW menurut Desa/Kelurahan di Kecamatan {pilihkec}, {pilihkab}")
    st.text("Sumber Data: Pemutakhiran MFD Semester 1 2023")
    kol1d, kol1e, kol1f = st.columns(3)
    if pilihkab and pilihkec:
        tabelkk = datakk[(datakk['nmkab'] == pilihkab) & (datakk['nmkec'] == pilihkec)]
        tabelkk2 = tabelkk[['nmdesa', 'jumlah_rw', 'jumlah_rt']].sort_values(by='jumlah_rt', ascending=False)
        
        with kol1d:
            pie_kk = px.pie(tabelkk2, values='jumlah_rt', names='nmdesa', 
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
            bar_kk = px.bar(tabelkk2, x='nmdesa', y='jumlah_rt', color='nmdesa',
                            text='jumlah_rt',            
                            color_discrete_sequence=warna_options[pilihwarna])
            bar_kk.update_layout(showlegend=False)
            with st.container(border=True):
                st.plotly_chart(bar_kk, use_container_width=True)
        with kol1f:
            st.dataframe(tabelkk2, hide_index=True, use_container_width=True)
            st.subheader("", divider='rainbow')
            tabelseri = datakk[(datakk['nmkab'] == pilihkab) & (datakk['nmkec'] == pilihkec)]
            with st.expander("Lihat Tabel Seri"):
                st.dataframe(tabelseri, use_container_width=True, hide_index=True)

st.subheader("", divider='rainbow')
with st.container(border=True):
    st.info(f"Jumlah RT/ RW di Kecamatan {pilihkec}, {pilihkab}")
    kol2a, kol2b = st.columns(2)
    trimep = px.treemap(tabelkk, path=['nmkec', 'nmdesa'], values='jumlah_rt', 
                        color_discrete_sequence=warna_options[pilihwarna])
    trimep.update_traces(textinfo='label+value')
    
    sunburst = px.sunburst(tabelkk, path=['nmkec', 'nmdesa'], values='jumlah_rt', 
                        color_discrete_sequence=warna_options[pilihwarna])
    sunburst.update_traces(textinfo='label+value')
    
    with kol2a:
        with st.container(border=True):
            st.plotly_chart(trimep, use_container_width=True)
    
    with kol2b:
        with st.container(border=True):
            st.plotly_chart(sunburst, use_container_width=True)

st.subheader("", divider='rainbow')
        
# PERKEMBANGAN    
#with st.container(border=True):
#    st.info(f"Perkembangan Jumlah KK di Kecamatan {pilihkec}, {pilihkab}, menurut Desa/ Kelurahan")
#    datakk_kec = datakk.groupby(['nmkab', 'nmkec', 'tahun'])['jumlah_rt'].sum().reset_index()
    
#    kola, kolb, kolc = st.columns(3)
    
#    tren_kk = datakk[(datakk['nmkab'] == pilihkab) & (datakk['nmkec'] == pilihkec)]
#    area_kk = px.area(tren_kk, x='tahun', y='jumlah_rt', color='nmdesa', 
#                            color_discrete_sequence=warna_options[pilihwarna])
#    with kola:
#        with st.container(border=True):
#            st.plotly_chart(area_kk, use_container_width=True)
    
    
#    barkk = px.bar(tren_kk, x='tahun', y='jumlah_rt', color='nmdesa', 
#                            color_discrete_sequence=warna_options[pilihwarna])
#    with kolb:
#        with st.container(border=True):
#            st.plotly_chart(barkk, use_container_width=True)
    
    
#    line_kk = px.line(tren_kk, x='tahun', y='jumlah_rt', color='nmdesa', 
#                            color_discrete_sequence=warna_options[pilihwarna])
#    with kolc:
#        with st.container(border=True):
#            st.plotly_chart(line_kk, use_container_width=True)
    
st.link_button("sumber Data", url="https://frs.bps.go.id/area")
