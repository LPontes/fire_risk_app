import streamlit as st
from PIL import Image
import datetime as dt
import ee
import geemap as gee

# import geopandas as gpd
from src import riscodefogo as rdf

gee.ee_initialize()

silv = ee.FeatureCollection("projects/ee-lucaspontesm/assets/silvicultura_2021_clean50");

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
    rf = rdf.risco_basico(pse)
    rf = rdf.risco_observado(rf, begTime)
    rf = rdf.risco_ajustado(rf, begTime)
    rf = rdf.classifica_risco_de_fogo(rf)

    st.write(f"Data da análise: {begTime.strftime('%Y-%m-%d')}")
    
    image = Image.open('./assets/legenda_RF.jpg')
    st.image(image, caption='Legenda: classes de risco de fogo')

    palette = [
            '000096','0064ff', '00b4ff', '33db80', '9beb4a',
            'ffeb00', 'ffb300', 'ff6400', 'eb1e00', 'af0000'
            ]

    precipitationVis = {'min': 0, 'max': 100, 'palette': palette}
    vis_classe_fogo = {'min': 1, 'max': 5, 'palette': ['green', 'lime', 'yellow', 'red', 'maroon']}

    m = gee.Map()
    m.add_basemap("ROADMAP")
    m.addLayer(pse, precipitationVis, 'Dias de Secura (PSE)')
    m.addLayer(rf, vis_classe_fogo, 'Risco de Fogo Observado')
    m.addLayer(silv, {},'Áreas de silvicultura')
    m.setCenter(-48, -24, 6.5)  
    m.to_streamlit(height=500)

    st.title('About')
    st.info(
        """
        Esse web app foi criado por [Lucas Pontes](https://github.com/LPontes).
        Acesse meu [portfólio](https://github.com/LPontes/Portfolio).
            
        A documentação completa pode ser acessada em: <https://github.com/LPontes/streamlit_demo>
    """
    )


    # @st.cache
    # def risco_calc():
    #     pse, begTime = rdf.dias_de_seca()
    #     rb = rdf.risco_basico(pse)
    #     ro = rdf.risco_observado(rb, begTime)
    #     rf = rdf.risco_ajustado(ro, begTime)

    #     return rf
    
    # rf = risco_calc()