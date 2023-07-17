import streamlit as st
import ee
import geemap as gee
import datetime 

gee.ee_initialize()

def app():
    st.title("Monitoramento do Risco de Incêndio")

    st.markdown(
        """
        Risco de fogo ou incêndio estimado de acordo com metodologia do INPE,
          com base em dados meteorológicos e de uso e cobertura do solo
    """
    )
    
    begTime = st.date_input("Selecione a data", datetime.date.today())
    
    lulc = ee.Image("projects/ee-lucaspontesm/assets/MAPBIOMAS/mapbiomas-brazil-collection-71-saopaulo-2021")
    
    m = gee.Map()
    m.addLayer(lulc)
    m.add_basemap("ROADMAP")
    m.to_streamlit(height=700)
