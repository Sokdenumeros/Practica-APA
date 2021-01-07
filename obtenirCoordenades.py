import pandas as pd
import pickle
from geopy.geocoders import Nominatim

df = pd.read_csv('fires-all.csv')

coordMunicipio = pd.Series(None, index=df['municipio'].unique()).to_dict()

error = []
geolocator = Nominatim(user_agent="apaProject")
for municipio in coordMunicipio.keys():
    try:
        # print(municipio)
        # print(type(municipio))
        if '/' in municipio:
            raise Exception
        location = geolocator.geocode(municipio)
        if 'España' not in location.address:
            print("Not in Spain: ", municipio)
            raise Exception
        coordMunicipio[municipio] = (location.latitude, location.longitude)

    except:
        error.append(municipio)


pickle.dump(coordMunicipio, open("coordenadesMunicipis.p", "wb"))

print("Llista municipis no trobats:")
print(error)
