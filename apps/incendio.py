import streamlit as st
import ee
import geemap as gee
import datetime as dt
import geopandas as gpd
from src import riscodefogo as rdf

gee.ee_initialize()

def app():
    st.title("Monitoramento do Risco de Incêndio")

    st.markdown(
        """
        Risco de fogo para o estado de São Paulo.
         Adaptado da metodologia do [INPE](https://queimadas.dgi.inpe.br/~rqueimadas/documentos/RiscoFogo_Sucinto.pdf),
          com base em dados meteorológicos e de uso e cobertura do solo
        """
    )

    # st.write(f"{os.getcwd()}")
    
    begTime = st.date_input("Selecione a data", dt.date.today())
    pse = rdf.dias_de_seca(begTime)
    rb = rdf.risco_basico(pse)

    palette = [
    '000096','0064ff', '00b4ff', '33db80', '9beb4a',
    'ffeb00', 'ffb300', 'ff6400', 'eb1e00', 'af0000'
    ]
    m = gee.Map()
    m.add_basemap("ROADMAP")
    fpVis = {'min': 0, 'max': 1, 'palette': palette}
    m.addLayer(rb, fpVis, 'Risco Básico de Fogo')
    m.setCenter(-48, -24, 6)  
    m.to_streamlit(height=700)