import streamlit as st
import geopandas
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static # Untuk menampilkan peta folium di Streamlit

# --- Fungsi untuk membuat data dummy (ini akan diganti dengan read_file() di aplikasi nyata) ---
@st.cache_data # Cache data agar tidak di-load ulang setiap kali Streamlit refresh
def baca_data():
    polygons_data = "data/petakecamatan.geojson"
    gdf = geopandas.read_file(polygons_data, crs="EPSG:4326")
    return gdf

# --- Fungsi Utama Aplikasi Streamlit ---
def main():
    st.set_page_config(layout="wide") # Menggunakan layout lebar untuk peta
    st.title("Bab 1. Kondisi Geografi")
    st.subheader("", divider='orange')

    # Memuat data
    gdf = baca_data()
    gdf['kdkab'] = gdf['kdkab'].astype(str)
    condition = gdf['kdkab'].str[:1] != '7'
    gdf.loc[condition, 'nmkab'] = 'KABUPATEN ' + gdf['nmkab']
    
    col_select1, col_select2 = st.columns(2) # Kolom untuk selection box di bagian atas
    
    # --- Bagian 1: Pemilihan Kabupaten ---
    unique_kabupaten = gdf['nmkab'].unique().tolist()
    
    with col_select1:
        selected_kabupaten = st.selectbox(
            "Pilih Kabupaten:",
            options=[''] + unique_kabupaten, # Tambahkan opsi kosong
            index=0 # Default ke opsi kosong
        )

    selected_kecamatan = None
    if selected_kabupaten:
        # Filter kecamatan berdasarkan kabupaten yang dipilih
        kecamatan_in_kabupaten = gdf[gdf['nmkab'] == selected_kabupaten]['nmkec'].unique().tolist()
        
        # --- Bagian 2: Pemilihan Kecamatan ---
        with col_select2:
            selected_kecamatan = st.selectbox(
                f"Pilih Kecamatan:",
                options=[''] + kecamatan_in_kabupaten, # Tambahkan opsi kosong
                index=0
            )

    st.markdown("---") # Garis pemisah

    # --- Bagian 3: Menampilkan Batas Kecamatan Terpilih ---
    if selected_kecamatan:
        st.subheader(f"Kondisi Geografi Kecamatan {selected_kecamatan.title()}, {selected_kabupaten.title()}")

        # Dapatkan poligon target
        target_polygon_row = gdf[(gdf['nmkec'] == selected_kecamatan) & (gdf['nmkab'] == selected_kabupaten)].iloc[0]
        target_geometry = target_polygon_row.geometry
        target_centroid = target_geometry.centroid
        
        # Mengambil koordinat dari MultiPolygon sebagai list datar (x,y)
        coords = []
        if target_geometry.geom_type == "MultiPolygon":
            for polygon in target_geometry.geoms:
                for ring in polygon.exterior.coords:
                    coords.append(ring)
        elif target_geometry.geom_type == "Polygon":
            for ring in target_geometry.exterior.coords:
                coords.append(ring)

        # Extract x (longitude) dan y (latitude)
        longitudes = [c[0] for c in coords]
        latitudes = [c[1] for c in coords]

        # Cari nilai terkecil dan terbesar
        min_lat = min(latitudes)
        max_lat = max(latitudes)
        min_lon = min(longitudes)
        max_lon = max(longitudes)

        # Format string informasi astronomis
        astronomis_info_id = (
            f"Lokasi astronomis Kecamatan {selected_kecamatan.title()} berada di "
            f"{min_lat:.4f} sampai {max_lat:.4f} derajat lintang selatan dan "
            f"{min_lon:.4f} sampai {max_lon:.4f} derajat bujur timur."
        )

        astronomis_info_en = (
            f"The astronomical location of {selected_kecamatan.title()} subdistrict ranges from "
            f"{min_lat:.4f} to {max_lat:.4f} degrees south latitude and "
            f"{min_lon:.4f} to {max_lon:.4f} degrees east longitude."
        )

        
        luaskec1 = round(gdf[gdf['nmkec'] == selected_kecamatan]['luas'].sum() / 1000000, 2)
        
        luaskec2 = round(gdf[gdf['nmkec'] == selected_kecamatan]['luas'].sum() / 10000, 2)

        # Temukan poligon yang berbatasan (seluruhnya di GeoDataFrame)
        # Penting: Pastikan tidak membandingkan dengan dirinya sendiri
        touches_mask = gdf.geometry.touches(target_geometry) & \
                       ((gdf['nmkec'] != selected_kecamatan) | (gdf['nmkab'] != selected_kabupaten)) # Exclude self
        
        # Filter hanya poligon yang berbatasan
        bordering_polygons_gdf = gdf[touches_mask].copy()

        # Inisialisasi dictionary untuk menyimpan hasil
        result_boundaries_id = {
            'Utara': [],
            'Selatan': [],
            'Barat': [],
            'Timur': []
        }
        
        result_boundaries_en = {
            'North': [],
            'South': [],
            'West': [],
            'East': []
        }
        
        direction_map_id_to_en = {
            'Utara': 'North',
            'Selatan': 'South',
            'Barat': 'West',
            'Timur': 'East'
        }


        if not bordering_polygons_gdf.empty:
            for index, row in bordering_polygons_gdf.iterrows():
                other_geometry = row.geometry
                other_centroid = other_geometry.centroid

                # Format string nama kecamatan/kabupaten (Bahasa Indonesia)
                if row['nmkab'] == selected_kabupaten:
                    name_to_display_id = f"Kecamatan {row['nmkec'].title()}"
                    name_to_display_en = f"{row['nmkec'].title()} Subdistrict"
                else:
                    name_to_display_id = f"Kecamatan {row['nmkec'].title()} ({row['nmkab'].title()})"
                    name_to_display_en = f"{row['nmkec'].title()} Subdistrict ({row['nmkab'].title()})"

                # Tentukan arah relatif berdasarkan posisi centroid
                # Batas Utara/Selatan
                if other_centroid.y > target_centroid.y:
                    result_boundaries_id['Utara'].append(name_to_display_id)
                    result_boundaries_en['North'].append(name_to_display_en)
                elif other_centroid.y < target_centroid.y:
                    result_boundaries_id['Selatan'].append(name_to_display_id)
                    result_boundaries_en['South'].append(name_to_display_en)

                # Batas Timur/Barat
                if other_centroid.x > target_centroid.x:
                    result_boundaries_id['Timur'].append(name_to_display_id)
                    result_boundaries_en['East'].append(name_to_display_en)
                elif other_centroid.x < target_centroid.x:
                    result_boundaries_id['Barat'].append(name_to_display_id)
                    result_boundaries_en['West'].append(name_to_display_en)
            
            # --- Tampilkan hasil dalam 2 kolom teratas ---
            col_content1, col_content2 = st.columns(2)
            
            with col_content1:
                with st.container(border=True):
                    st.subheader("**GEOGRAFI**")
                    
                    st.write(f"Kecamatan {selected_kecamatan.title()} adalah salah satu kecamatan di {selected_kabupaten.title()} dengan luas wilayah {luaskec1} kilometer persegi atau {luaskec2} hektar.")
                    
                    st.write(astronomis_info_id)
                    
                    st.write(f"Berdasarkan posisi geografisnya, Kecamatan {selected_kecamatan.title()} memiliki batas-batas:")
                    for direction_id, names_id in result_boundaries_id.items():
                        if names_id:
                            st.markdown(f"- **{direction_id}**: {', '.join(sorted(set(names_id)))}")
                        else:
                            st.markdown(f"- **{direction_id}**: Tidak ada")

            with col_content2:
                with st.container(border=True):
                    st.subheader("**GEOGRAPHY**")
                    
                    st.write(f"The {selected_kecamatan.title()} subdistrict is one of the subdistricts in {selected_kabupaten.title()} with an area of {luaskec1} square kilometers or {luaskec2} hectares.")
                    
                    st.write(astronomis_info_en)
                
                    st.write(f"Based on its geographical position, the {selected_kecamatan.title()} subdistrict has the following boundaries:")

                    for direction_en, names_en in result_boundaries_en.items():
                        if names_en:
                            st.markdown(f"- **{direction_en}**: {', '.join(sorted(set(names_en)))}")
                        else:
                            st.markdown(f"- **{direction_en}**: None")

            st.markdown("---") # Garis pemisah sebelum peta

            # --- Visualisasi Peta dengan Folium (di bagian bawah) ---
            st.write(f"**Peta Kecamatan {selected_kecamatan.title()}:**")
            
            # Buat peta folium
            m = folium.Map(location=[target_centroid.y, target_centroid.x], zoom_start=11)

            # Tambahkan poligon target ke peta
            folium.GeoJson(
                target_geometry.__geo_interface__,
                name=selected_kecamatan,
                style_function=lambda x: {'fillColor': '#ff7800', 'color': 'black', 'weight': 2, 'fillOpacity': 0.7}
            ).add_to(m)

            # Tambahkan poligon yang berbatasan ke peta
            if not bordering_polygons_gdf.empty:
                folium.GeoJson(
                    bordering_polygons_gdf.__geo_interface__,
                    name="Berbatasan",
                    style_function=lambda x: {'fillColor': '#0078ff', 'color': 'black', 'weight': 1, 'fillOpacity': 0.5}
                ).add_to(m)
            
            # Tambahkan kontrol layer untuk on/off layer
            folium.LayerControl().add_to(m)

            # Tampilkan peta di Streamlit
            folium_static(m, width=1000, height=600) # Lebarkan peta untuk tampilan yang lebih baik
            
            st.caption("Sumber: https://github.com/Alf-Anas/batas-administrasi-indonesia")

        else:
            st.warning(f"Tidak ada poligon lain yang secara langsung berbatasan dengan '{selected_kecamatan}'.")
    elif selected_kabupaten:
        st.info("Silakan memilih Kecamatan untuk melihat batas-batas wilayahnya.")
    else:
        st.info("Silakan memilih Kabupaten terlebih dahulu.")

# Panggil fungsi utama saat script dijalankan
if __name__ == "__main__":
    main()
