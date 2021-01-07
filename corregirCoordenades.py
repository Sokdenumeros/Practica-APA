import pickle
import pandas as pd
from geopy.distance import geodesic
import statistics as stat

df = pd.read_csv('fires-all.csv')
coords = pickle.load(open("coordenadesMunicipis.p", 'rb'))

notInCoordNewDict = {}

for index, row in df.iterrows():
    municipi = row['municipio']
    # Casos especials municipis amb el mateix nom
    if municipi == 'SOBRADO' and row['idmunicipio'] == 80:
        municipi = 'SOBRADOA'
        continue
    elif municipi == 'CIEZA' and row['idmunicipio'] == 19:
        municipi = 'CIEZAA'
        continue
    elif municipi == 'CASTEJÓN' and row['idmunicipio'] == 67:
        municipi = 'CASTEJONA'
        continue
    elif municipi == 'MOYA' and row['idmunicipio'] == 13:
        municipi = 'MOYAA'
        if row['lng'] - 15.582590 > 1:
            row['lng'] = -15.582590
        continue
    elif municipi == 'ARROYOMOLINOS' and row['idmunicipio'] == 23:
        municipi = 'ARROYOMOLINOSA'
        continue
    elif municipi == "SANCTI-SPIRITUS" or municipi == "SANCTI-SPÍRITUS":
        continue

    # Municipi in dictionary
    if type(coords[municipi]) is tuple:
        # Comparem les coordenades del row amb les del diccionari mirant la distància geodèsica entre, si és major
        # a 25km les actualitzarem amb el valor del diccionari i posant explicit a 0
        # print("old2", geodesic(coords[municipi], (df.at[index, "lat"], df.at[index, "lng"])).km)
        if geodesic(coords[municipi], (row["lat"], row["lng"])).km > 25:
            df.at[index, "lat"] = coords[municipi][0]
            df.at[index, "lng"] = coords[municipi][1]
            df.at[index, "latlng_explicit"] = 0
    # Municipi not in dictionary, fer la median amb els municipis i posant explicit a 0
    else:
        if municipi not in notInCoordNewDict:
            rowsMunicipi = df.loc[df['municipio'] == municipi]
            notInCoordNewDict[municipi] = (stat.median(rowsMunicipi["lat"]), stat.median(rowsMunicipi["lng"]))

        df.at[index, "lat"] = notInCoordNewDict[municipi][0]
        df.at[index, "lng"] = notInCoordNewDict[municipi][1]
        df.at[index, "latlng_explicit"] = 0

df.to_csv('coordsCorregides.csv', index=False)
