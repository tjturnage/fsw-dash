#############################################
### This file is not currently being used ###

#The plan moving forward is to create a CWA chlorpleth map
# Examples here: https://plotly.com/python/county-choropleth/

#############################################


import json
import plotly.express as px
import random
import pandas as pd
import plotly.express as px
import geopandas as gpd

cwa_map_path = 'C:/data/GIS/conus_cwas_new.geojson'
gdf = gpd.read_file(cwa_map_path)
gdf = gdf.set_index("CWA")

fig = px.choropleth_mapbox(gdf,
                           geojson=gdf.geometry,
                           locations=gdf.index,
                           color="Joly",
                           center={"lat": 45.5517, "lon": -73.7073},
                           mapbox_style="open-street-map",
                           zoom=8.5)
fig.show()

# all_afds = ['AFDABQ', 'AFDABR', 'AFDAFC', 'AFDAFG', 'AFDAJK',\
#                                 'AFDAKQ', 'AFDALY', 'AFDAMA', 'AFDAPX', 'AFDARX',\
#                                 'AFDBGM', 'AFDBIS', 'AFDBMX', 'AFDBOI', 'AFDBOU',\
#                                 'AFDBOX', 'AFDBRO', 'AFDBTV', 'AFDBUF', 'AFDBYZ',\
#                                 'AFDCAE', 'AFDCAR', 'AFDCHS', 'AFDCLE', 'AFDCRP',\
#                                 'AFDCTP', 'AFDCYS', 'AFDDDC', 'AFDDLH', 'AFDDMX',\
#                                 'AFDDPQ', 'AFDDTX', 'AFDDVN', 'AFDEAX', 'AFDEKA',\
#                                 'AFDEPZ', 'AFDEWX', 'AFDEYW', 'AFDFFC', 'AFDFGF',\
#                                 'AFDFGZ', 'AFDFSD', 'AFDFWD', 'AFDGGW', 'AFDGID',\
#                                 'AFDGJT', 'AFDGLD', 'AFDGRB', 'AFDGRR', 'AFDGSP',\
#                                 'AFDGYX', 'AFDHFO', 'AFDHGX', 'AFDHNX', 'AFDHUN',\
#                                 'AFDICT', 'AFDILM', 'AFDILN', 'AFDILX', 'AFDIND',\
#                                 'AFDIWX', 'AFDJAN', 'AFDJAX', 'AFDJKL', 'AFDKEY',\
#                                 'AFDLBF', 'AFDLCH', 'AFDLIX', 'AFDLKN', 'AFDLMK',\
#                                 'AFDLOT', 'AFDLOX', 'AFDLSX', 'AFDLUB', 'AFDLWX',\
#                                 'AFDLZK', 'AFDMAF', 'AFDMEG', 'AFDMFL', 'AFDMFR',\
#                                 'AFDMHX', 'AFDMKX', 'AFDMLB', 'AFDMOB', 'AFDMPX',\
#                                 'AFDMQT', 'AFDMRX', 'AFDMSO', 'AFDMTR', 'AFDOAX',\
#                                 'AFDOHX', 'AFDOKX', 'AFDOTX', 'AFDOUN', 'AFDPAH',\
#                                 'AFDPBZ', 'AFDPDT', 'AFDPHI', 'AFDPIH', 'AFDPPG',\
#                                 'AFDPQ', 'AFDPQR', 'AFDPSR', 'AFDPUB', 'AFDRAH',\
#                                 'AFDREV', 'AFDRIW', 'AFDRLX', 'AFDRNK', 'AFDSDF',\
#                                 'AFDSEW', 'AFDSGF', 'AFDSGX', 'AFDSHV', 'AFDSJT',\
#                                 'AFDSJU', 'AFDSLC', 'AFDSTO', 'AFDTAE', 'AFDTBW',\
#                                 'AFDTFX', 'AFDTOP', 'AFDTSA', 'AFDTWC', 'AFDUNR',\
#                                 'AFDVEF']

# cwa_list = [x[3:] for x in all_afds]
# number_list = [random.randint(0, 100) for y in all_afds]


# df = pd.DataFrame(list(zip(cwa_list, number_list)),
#                columns =['CWA', 'count'])

# print(df)

# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
