import pickle
import pandas as pd
import numpy as np
from geopy.distance import geodesic
import statistics as stat
import math

df = pd.read_csv('fires-all.csv')
coords = pickle.load(open("coordenadesMunicipis.p", 'rb'))

corregirMa = []
i = 0
for index, row in df.iterrows():
# for municipi, coord in coords.items():
    municipi = row['municipio']
    # Municipi in dictionary
    if municipi in coords:
        # Iterem totes les files del municipi i les que no concordin amb el diccionari comprovant la distància entre
        # el diccionari i la distància del row i
        # les actualitzarem amb
        # el valor del diccionari i posant explicit a 0
        if geodesic(coords[municipi], (row["lat"], row["lng"])).km > 25:
            df.at[row["id"], "lat"] = coords[municipi][0]
            df.at[row["id"], "lng"] = coords[municipi][1]
            df.at[row["id"], "latlng_explicit"] = 0
    # Municipi not in dictionary, fer mitjana amb els municipis (treient els màx i minim) i posant explicit a 0
    else:
        pass
    # rowsMunicipi = df.loc[df['municipio'] == municipi]
    # varLat = np.var(rowsMunicipi["lat"])
    # varLng = np.var(rowsMunicipi["lng"])
    # # print(coordMunicipi)
    # print("Municipi:", municipi, "Lat var:", varLat, "Lng var:", varLng)

    # Municipis amb el mateix nom, els id són diferent i coord correcte per tant modifiquem el nom del
    # municipi posant per exemple SOBRADOA i SOBRADOB per distingir el municipi de SOBRADO
    # if municipi == "SOBRADO" or municipi == "CIEZA" or municipi == "CASTEJÓN" or municipi == "MOYA":
    #     print(municipi)
    #
    # if varLng > 1 or varLat > 1:
    #     i += 1
    #     # Cas 1: No està al diccionari
    #     if type(coord) is not tuple:
    #         # Fer mitjana amb els municipis (treient els màx i minim) i posant explicit a 0
    #
    #         continue
    #     else:
    #         # Iterem totes les files del municipi i les que no concordin amb el diccionari comprovant la distància entre
    #         # el diccionari i la distància del row i
    #         # les actualitzarem amb
    #         # el valor del diccionari i posant explicit a 0
    #         for row in rowsMunicipi:
    #             if distance.vincenty(coord, (row["lat"], row["lng"])) > 25:
    #                 df.at[row["id"], "lat"] = coord[0]
    #                 df.at[row["id"], "lng"] = coord[1]
    #
    #
    #                 pass
    #         pass

        # print(modaLat, modaLng)
        # print(coord)
        # print(coord[0], coord[1])
        # print("Problem")
        # print(municipi)
        # print(coordMunicipi)
        # break
    # if i > 50:
    #     break

print("Fucked:", i)
print("CorregirMa", len(corregirMa), corregirMa)
