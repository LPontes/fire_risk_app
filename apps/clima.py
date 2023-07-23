import streamlit as st
import leafmap.foliumap as leafmap
import ee
import geemap as gee
import datetime as dt
gee.ee_initialize()
import geopandas as gpd
from src import riscos_climaticos as rc

df_uf = gpd.read_file('./data/vector/uf_sp.shp')
# df_br =  gpd.read_file('./data/vector/br.shp')
# bbox = ee.Geometry.Polygon(list(df_uf[df_uf['SIGLA_UF']=='SP'].envelope.geometry.exterior[0].coords))
aoi = ee.Geometry.Polygon(list(df_uf[df_uf['SIGLA_UF']=='SP'].geometry.exterior[0].coords))
# aoi = ee.Feature("projects/ee-lucaspontesm/assets/uf_sp").geometry(); 
# br = ee.Geometry.Polygon(list(df_br.geometry.exterior[0].coords))

palette = ['000096','0064ff', '00b4ff', '33db80', '9beb4a',
           'ffeb00', 'ffb300', 'ff6400', 'eb1e00', 'af0000']

palette_reverse = ['a50026', 'd73027', 'f46d43', 'fdae61', 'fee090', 
  'e0f3f8', 'abd9e9', '74add1', '4575b4', '313695']

vis_dict = {'Velocidade do vento (m/s)': {'min': 0, 'max': 15, 'palette': palette},
            'Temperatura mínima (ºC)':{'min': -5, 'max': 35, 'palette': palette},
            'Umidade relativa do ar (%)':{'min': 15, 'max': 100, 'palette': palette_reverse},
            'Precipitação (mm)':{'min': 0, 'max': 100, 'palette': palette}}

def app():
    st.title('Riscos Meteorológicos')
    begTime = dt.date.today()

    delta_date = st.sidebar.slider('Selecione a variação da data',
                            min_value=0,
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
    
    varVis = vis_dict[var_name]
    predict_date = begTime + dt.timedelta(days=delta_date)

    var_to_plot = rc.gfs_var_prediction(var_name, predict_date, aoi)

    st.write(f"Data da análise: {predict_date.strftime('%Y-%m-%d')}")

    m = gee.Map()
    m.addLayer(var_to_plot, varVis)
    m.setCenter(-47.4, -22.8, 7)
    # m.add_colorbar_branca(colors=palette, vmin=0, vmax=100, layer_name="Layer 3")
    m.to_streamlit(height=500)

    st.title('About')
    st.info(
        """
        Esse web app foi criado por [Lucas Pontes](https://github.com/LPontes).
        Acesse meu [portfólio](https://github.com/LPontes/Portfolio).
            
        A documentação completa pode ser acessada em: <https://github.com/LPontes/streamlit_demo>
    """
    )
