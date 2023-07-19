import ee
import geemap as gee
import datetime as dt
gee.ee_initialize()


gfs_collection = ee.ImageCollection('NOAA/GFS0P25')

def gfs_var_prediction(var_name, predict_date, bbox):
    
    choose_hours_dict = {1:[0,23],
                        2:[24,47],
                        3:[48,73]}
    
    var_dict = {'Velocidade do vento (m/s)': ['u_component_of_wind_10m_above_ground',
                                              'v_component_of_wind_10m_above_ground'],
                'Temperatura mínima (ºC)':'temperature_2m_above_ground',
                'Umidade relativa do ar (%)':'relative_humidity_2m_above_ground',
                'Precipitação (mm)':'total_precipitation_surface'}

    delta_time = (predict_date - dt.date.today()).days

    # Defini os inputs de tempo
    if delta_time > 0:
        today = ee.Date(dt.date.today().strftime("%Y-%m-%d"))
        max_advance = 3
        ti = choose_hours_dict[delta_time][0]
        tf = choose_hours_dict[delta_time][1]
    else:
        delta_time += -1 # força usar a previsao gerada no dia anterior ao que se quer observar
        today = ee.Date((dt.date.today() + dt.timedelta(days=delta_time)).strftime("%Y-%m-%d"))
        max_advance = 1
        ti = choose_hours_dict[1][0]
        tf = choose_hours_dict[1][1]

    # Calcula das predicoes
    # velocidade do vento é feito separado nesse primeiro if
    if var_name == 'Velocidade do vento (m/s)':
        var_pred = (gfs_collection
                    .select(['u_component_of_wind_10m_above_ground', 'v_component_of_wind_10m_above_ground'])
                    .filterDate(today, today.advance(6,'hour')) # get a specific forecast initialization,
                    .filter(ee.Filter.lt('forecast_time',today.advance(max_advance,'day').millis())) # Quantos dias pra frente
                    .filter(ee.Filter.gte('forecast_hours',ti) )
                    .filter(ee.Filter.lte('forecast_hours',tf))
                    .max()) # make a composite of the collection
  
        var_pred = var_pred.clip(bbox)
        # Wind speed
        var_pred = var_pred.pow(2).reduce(ee.Reducer.sum()).sqrt()
    
    # caso for outra variavel
    else:
        var_pred = (gfs_collection
                    .select(var_dict[var_name])
                    .filterDate(today, today.advance(6,'hour')) # get a specific forecast initialization,
                    .filter(ee.Filter.lt('forecast_time',today.advance(max_advance,'day').millis())) # Quantos dias pra frente
                    .filter(ee.Filter.gte('forecast_hours',ti) )
                    .filter(ee.Filter.lte('forecast_hours',tf))
                    .max()) # make a composite of the collection
  
        var_pred = var_pred.clip(bbox)
        
    return var_pred