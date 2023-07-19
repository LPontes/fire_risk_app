import streamlit as st
import leafmap.foliumap as leafmap
import ee
import geemap as gee
import datetime as dt
gee.ee_initialize()
import geopandas as gpd
from src import riscos_climaticos as rc

df_uf = gpd.read_file('./data/vector/uf_sp.shp')
df_br =  gpd.read_file('./data/vector/br.shp')
bbox = ee.Geometry.Polygon(list(df_uf[df_uf['SIGLA_UF']=='SP'].envelope.geometry.exterior[0].coords))
aoi = ee.Geometry.Polygon(list(df_uf[df_uf['SIGLA_UF']=='SP'].geometry.exterior[0].coords))
br = ee.Geometry.Polygon(list(df_br.geometry.exterior[0].coords))

def app():
    st.title('Riscos Meteorológicos')
    begTime = dt.date.today()

    delta_date = st.sidebar.slider('Selecione a variação da data',
                            min_value=-10,
                            max_value=3,
                            value=0,
                            step=1,
                            help='0: dia atual, números negativos: dias passados, 1-3: previsão para os próximos dias'
                            )
    
    var_name = st.sidebar.selectbox('Selecione a variável climática de interesse',
                            ('Velocidade do vento (m/s)',
                            'Temperatura mínima (ºC)',
                            'Umidade relativa do ar (%)',
                            'Precipitação (mm)')
                            )
                        
    predict_date = begTime + dt.timedelta(days=delta_date)
    var_to_plot = rc.gfs_var_prediction(var_name, predict_date, br)

    st.write(f"Data da análise: {predict_date.strftime('%Y-%m-%d')}")
                    
    palette = ['000096','0064ff', '00b4ff', '33db80', '9beb4a',
               'ffeb00', 'ffb300', 'ff6400', 'eb1e00', 'af0000']

    precipitationVis = {'min': 0, 'max': 30, 'palette': palette}

    m = gee.Map()
    m.addLayer(var_to_plot, precipitationVis)
    m.setCenter(-50, -31, 4)
    m.to_streamlit(height=500)

    st.title('About')
    st.info(
        """
        Esse web app foi criado por [Lucas Pontes](https://github.com/LPontes).
        Acesse meu [portfólio](https://github.com/LPontes/Portfolio).
            
        A documentação completa pode ser acessada em: <https://github.com/LPontes/streamlit_demo>
    """
    )
