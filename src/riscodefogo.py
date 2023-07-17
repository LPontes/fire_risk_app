import geopandas as gpd
import ee
import geemap as gee
import datetime as dt
gee.ee_initialize()

## Read 
df_uf = gpd.read_file('./data/vector/uf_sp.shp')
aoi = ee.Geometry.Polygon(list(df_uf[df_uf['SIGLA_UF']=='SP'].geometry.exterior[0].coords))
lulc = ee.Image("projects/ee-lucaspontesm/assets/MAPBIOMAS/mapbiomas-brazil-collection-71-saopaulo-2021")
imerg_collection = ee.ImageCollection("NASA/GPM_L3/IMERG_V06")
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
                'defaultValue': 0,
                'bandName': 'b1'
                })

def dias_de_seca(begTime, aoi=aoi):
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
    
    # trata casos em que nao exista dados de precipitacao para o dia selecionado
    if len(p1.getInfo()['bands']) == 0:
        p1 = p2.multiply(0)

    fp1 = p1.expression('exp(-0.14 *p1)',
                    {'p1': p1.select('precipitationCal')})

    fp2 = p2.expression('exp(-0.07 *(p2-p1))',
                        {'p1': p1.select('precipitationCal'),
                        'p2': p2.select('precipitationCal')})

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
    
    return pse

def risco_basico(pse):
    rb = pse.expression('0.8*(1+sin((((a*pse)-90))*(3.14/180)))',
                        {'a':flamability.select('remapped'),
                         'pse': pse.select('constant')}
                         )   
    return rb