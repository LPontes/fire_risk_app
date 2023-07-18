import streamlit as st
from PIL import Image
import datetime as dt

# import ee
import geemap as gee

# import geopandas as gpd
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

    pse, begTime = rdf.dias_de_seca()
    rb = rdf.risco_basico(pse)
    ro = rdf.risco_observado(rb, begTime)
    rf = rdf.risco_ajustado(ro, begTime)

    st.write(f"Data da análise: {begTime.strftime('%Y-%m-%d')}")
    
    image = Image.open('./assets/legenda_RF.jpg')
    st.image(image, caption='Legenda: classes de risco de fogo')

    palette = [
    '000096','0064ff', '00b4ff', '33db80', '9beb4a',
    'ffeb00', 'ffb300', 'ff6400', 'eb1e00', 'af0000'
    ]

    precipitationVis = {'min': 0, 'max': 100, 'palette': palette}
    vis_classe_fogo = {'min': 0, 'max': 1, 'palette': ['green', 'lime', 'yellow', 'red', 'maroon']}

    m = gee.Map()
    m.add_basemap("ROADMAP")
    m.addLayer(pse, precipitationVis, 'Dias de Secura (PSE)')
    m.addLayer(rf, vis_classe_fogo, 'Risco de Fogo Observado')
    m.setCenter(-48, -24, 7)  
    m.to_streamlit(height=700)