import geopandas as gpd
import ee
import geemap as gee
import datetime as dt
gee.ee_initialize()

## SETUP
begTime = dt.date.today()

## READ 
df_uf = gpd.read_file('./data/vector/uf_sp.shp')
aoi = ee.Geometry.Polygon(list(df_uf[df_uf['SIGLA_UF']=='SP'].geometry.exterior[0].coords))

lulc = ee.Image("projects/ee-lucaspontesm/assets/MAPBIOMAS/mapbiomas-brazil-collection-71-saopaulo-2021")
gfs_collection = ee.ImageCollection('NOAA/GFS0P25')
imerg_collection = ee.ImageCollection("NASA/GPM_L3/IMERG_V06")
viirs_collection = ee.ImageCollection("NOAA/VIIRS/001/VNP14A1")
dem = ee.Image("CGIAR/SRTM90_V4")

flame_cte = {1: ["Forest", 2],
        2: ["Natural Forest", 2],
        3: ["Forest Formation", 2],
        4: ["Savanna Formation", 2.4],
        5: ["Magrove", 1.5],
        6: ["Áreas Naturales Inundables - Leñosas (Bosque Inundable)",1.5],
        9: ["Forest Plantation", 4],
        10: ["Non Forest Natural Formation", 2],
        11: ["Wetland",1.5],
        12: ["Grassland (Pastizal, Formación Herbácea)", 6],
        13: ["Other Non Forest Natural Formation", 2],
        14: ["Farming", 4],
        15: ["Pasture", 6],
        18: ["Agriculture",4],
        19: ["Temporary Crops (Herbaceas - Agricultura)",4],
        20: ["Sugar Cane",4],
        21: ["Mosaic of Agriculture and Pasture",5],
        35: ["Oil Palm",4],
        36: ["Perennial Crops",3],
        39: ["Soy Beans",4],
        40: ["Rice",4],
        41: ["Mosaic of Crops",4],
        46: ['Coffe',4],
        47: ['Citrus',4],
        48: ['Other Perennial Crops', 4],
        49: ['Wooded Sandbank Vegetation', 3],
        50: ['Herbaceous Sandbank Vegetation', 3],
        62: ["Cotton", 4]
        }

## Reclassifica o mapa de uso do solos 
fromList = list(flame_cte.keys())
toList =   [x[1] for x in flame_cte.values()]

# Replace pixel values in the image. 
flamability = lulc.remap(**{
                'from': fromList,
                'to': toList,
                'defaultValue': None,
                'bandName': 'b1'
                })

def dias_de_seca(begTime=begTime, aoi=aoi):
    p1 = (imerg_collection
        .filterDate((begTime - dt.timedelta(days=1)).strftime("%Y-%m-%d"),
                    begTime.strftime("%Y-%m-%d"))
            .select('precipitationCal')
            .sum()
            .clip(aoi))
    while len(p1.getInfo()['bands']) == 0:
        begTime = (begTime - dt.timedelta(days=1))
        today = ee.Date(begTime.strftime("%Y-%m-%d"))

        p1 = (imerg_collection
                .filterDate((begTime - dt.timedelta(days=1)).strftime("%Y-%m-%d"),
                                begTime.strftime("%Y-%m-%d"))
                .select('precipitationCal')
                .sum()
                .clip(aoi))

    p2 = (imerg_collection
        .filterDate((begTime - dt.timedelta(days=2)).strftime("%Y-%m-%d"),
                    begTime.strftime("%Y-%m-%d"))
            .select('precipitationCal')
            .sum()
            .clip(aoi))

    p3 = (imerg_collection
        .filterDate((begTime - dt.timedelta(days=3)).strftime("%Y-%m-%d"),
                    begTime.strftime("%Y-%m-%d"))
            .select('precipitationCal')
            .sum()
            .clip(aoi))

    p4 = (imerg_collection
        .filterDate((begTime - dt.timedelta(days=4)).strftime("%Y-%m-%d"),
                    begTime.strftime("%Y-%m-%d"))
            .select('precipitationCal')
            .sum()
            .clip(aoi))

    p5 = (imerg_collection
        .filterDate((begTime - dt.timedelta(days=5)).strftime("%Y-%m-%d"),
                    begTime.strftime("%Y-%m-%d"))
            .select('precipitationCal')
            .sum()
            .clip(aoi))
    p10 = (imerg_collection
        .filterDate((begTime - dt.timedelta(days=10)).strftime("%Y-%m-%d"),
                    begTime.strftime("%Y-%m-%d"))
            .select('precipitationCal')
            .sum()
            .clip(aoi))
    p15 = (imerg_collection
        .filterDate((begTime - dt.timedelta(days=15)).strftime("%Y-%m-%d"),
                    begTime.strftime("%Y-%m-%d"))
            .select('precipitationCal')
            .sum()
            .clip(aoi))
    p30 = (imerg_collection
        .filterDate((begTime - dt.timedelta(days=30)).strftime("%Y-%m-%d"),
                    begTime.strftime("%Y-%m-%d"))
            .select('precipitationCal')
            .sum()
            .clip(aoi))
    p60 = (imerg_collection
        .filterDate((begTime - dt.timedelta(days=60)).strftime("%Y-%m-%d"),
                    begTime.strftime("%Y-%m-%d"))
            .select('precipitationCal')
            .sum()
            .clip(aoi))
    p90 = (imerg_collection
        .filterDate((begTime - dt.timedelta(days=90)).strftime("%Y-%m-%d"),
                    begTime.strftime("%Y-%m-%d"))
            .select('precipitationCal')
            .sum()
            .clip(aoi))
    p120 = (imerg_collection
        .filterDate((begTime - dt.timedelta(days=120)).strftime("%Y-%m-%d"),
                    begTime.strftime("%Y-%m-%d"))
            .select('precipitationCal')
            .sum()
            .clip(aoi))
    

    fp1 = p1.expression('exp(-0.14 *p1)',
                    {'p1': p1.select('precipitationCal')})

    fp2 = p2.expression('exp(-0.07 *(pf-pi))',
                    {'pi': p1.select('precipitationCal'),
                     'pf': p2.select('precipitationCal')})

    fp3 = p3.expression('exp(c *(pf-pi))',
                        {'c':-0.04,
                        'pi': p2.select('precipitationCal'),
                        'pf': p3.select('precipitationCal')})

    fp4 = p4.expression('exp(c *(pf-pi))',
                        {'c':-0.03,
                        'pi': p3.select('precipitationCal'),
                        'pf': p4.select('precipitationCal')})

    fp5 = p5.expression('exp(c *(pf-pi))',
                        {'c':-0.02,
                        'pi': p4.select('precipitationCal'),
                        'pf': p5.select('precipitationCal')})

    fp6a10 = p10.expression('exp(c *(pf-pi))',
                        {'c':-0.01,
                        'pi': p5.select('precipitationCal'),
                        'pf': p10.select('precipitationCal')})

    fp11a15 = p15.expression('exp(c *(pf-pi))',
                        {'c':-0.008,
                        'pi': p10.select('precipitationCal'),
                        'pf': p15.select('precipitationCal')})

    fp16a30 = p30.expression('exp(c *(pf-pi))',
                        {'c':-0.004,
                        'pi': p15.select('precipitationCal'),
                        'pf': p30.select('precipitationCal')})

    fp31a60 = p60.expression('exp(c *(pf-pi))',
                        {'c':-0.002,
                        'pi': p30.select('precipitationCal'),
                        'pf': p60.select('precipitationCal')})

    fp61a90 = p90.expression('exp(c *(pf-pi))',
                        {'c':-0.001,
                        'pi': p60.select('precipitationCal'),
                        'pf': p90.select('precipitationCal')})

    fp91a120 = p120.expression('exp(c *(pf-pi))',
                        {'c':-0.0007,
                        'pi': p90.select('precipitationCal'),
                        'pf': p120.select('precipitationCal')})
    pse = (fp1
        .multiply(fp2)
        .multiply(fp3)
        .multiply(fp4)
        .multiply(fp5)
        .multiply(fp6a10)
        .multiply(fp11a15)
        .multiply(fp16a30)
        .multiply(fp31a60)
        .multiply(fp61a90)
        .multiply(fp91a120)
        .multiply(105))
    
    return pse, begTime

def risco_basico(pse):
    rb = pse.expression('0.8*(1+sin((((a*pse)-90))*(3.14/180)))/2',
                        {'a':flamability.select('remapped'),
                         'pse': pse.select('constant')}
                         )   
    return rb

def risco_observado(rb, begTime):
     temperature = (gfs_collection
                    .filter(ee.Filter.date(begTime.strftime("%Y-%m-%d")))
                    .select('temperature_2m_above_ground').max())
     
     relative_humidity = (gfs_collection
                          .filter(ee.Filter.date(begTime.strftime("%Y-%m-%d")))
                          .select('relative_humidity_2m_above_ground').min())
     
     ft = temperature.expression('(Tmax*0.02)+0.4', {'Tmax': temperature})
     fu = relative_humidity.expression('(UR * -0.006)+1.3', {'UR':relative_humidity})

     flat = rb.expression('1+abs(lat)*0.003', {'lat':rb.pixelLonLat().select('latitude')})
     felv = dem.expression('1+alt*0.00003', {'alt':dem.select('elevation')})

     rf = rb.multiply(ft).multiply(fu).multiply(flat).multiply(felv)

     return rf

def risco_ajustado(rf, begTime):
    today = ee.Date(begTime.strftime("%Y-%m-%d"))
    focos = (viirs_collection
                .filterDate(today.advance(-3, 'day'), today)
                .select('FireMask').max().gt(6).clip(aoi)
                .remap(**{
                        'from': [0,1],
                        'to': [1,2],
                        'defaultValue': None,
                        'bandName': 'FireMask'
                        })
                )

    rf_ajustado = rf.multiply(focos)

    return rf_ajustado
     
     