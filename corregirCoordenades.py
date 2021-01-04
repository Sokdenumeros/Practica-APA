import pickle
import pandas as pd
import numpy as np
import statistics as stat
import math

df = pd.read_csv('fires-all.csv')
coords = pickle.load(open("coordenadesMunicipis.p", 'rb'))

corregirMa = []
i = 0
for municipi, coord in coords.items():
    coordMunicipi = df.loc[df['municipio'] == municipi][{"lng", "lat"}]
    varLat = np.var(coordMunicipi["lat"])
    varLng = np.var(coordMunicipi["lng"])
    # print(coordMunicipi)
    # print("Municipi:", municipi, "Lat var:", varLat, "Lng var:", varLng)
    if varLng > 1 or varLat > 1:
        i += 1
        corregirMa.append(municipi)
        # Cas 1: No està al diccionari
        if type(coord) is not tuple:
            # Descartem tot el municipi
            # corregirMa.append(municipi)
            continue
        else:
            pass
            # Iterem totes les files del municipi i eliminem les que no concordin amb el diccionari

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
