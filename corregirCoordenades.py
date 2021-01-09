import pickle
from geopy.distance import geodesic
import statistics as stat
import numpy as np
import pandas as pd


def correctCoords(dataframe):
    coords = pickle.load(open("coordenadesMunicipis.p", 'rb'))

    notInCoordNewDict = {}

    for index, row in dataframe.iterrows():
        municipi = row['municipio']
        # Casos especials municipis amb el mateix nom
        if municipi == 'SOBRADO' and row['idmunicipio'] == 80:
            dataframe.at[index, "municipio"] = 'SOBRADOA'
            continue
        elif municipi == 'CIEZA' and row['idmunicipio'] == 19:
            dataframe.at[index, "municipio"] = 'CIEZAA'
            continue
        elif municipi == 'CASTEJÓN' and row['idmunicipio'] == 67:
            dataframe.at[index, "municipio"] = 'CASTEJONA'
            continue
        elif municipi == 'MOYA' and row['idmunicipio'] == 13:
            dataframe.at[index, "municipio"] = 'MOYAA'
            if row['lng'] - 15.582590 > 1:
                row['lng'] = -15.582590
            continue
        elif municipi == 'ARROYOMOLINOS' and row['idmunicipio'] == 23:
            dataframe.at[index, "municipio"] = 'ARROYOMOLINOSA'
            continue
        elif municipi == "SANCTI-SPIRITUS" or municipi == "SANCTI-SPÍRITUS":
            continue
        # Cas especial municipi sense coordenades
        elif municipi == "BERA/VERA DE BIDASOA":
            if row["latlng_explicit"] == 0:
                dataframe.at[index, "lat"] = 43.281328
                dataframe.at[index, "lng"] = -1.679647
                dataframe.at[index, "latlng_explicit"] = 0
            continue

        # Municipi in dictionary
        if type(coords[municipi]) is tuple:
            # Comparem les coordenades del row amb les del diccionari mirant la distància geodèsica entre, si és major
            # a 25km les actualitzarem amb el valor del diccionari i posant explicit a 0
            if geodesic(coords[municipi], (row["lat"], row["lng"])).km > 25:
                dataframe.at[index, "lat"] = coords[municipi][0]
                dataframe.at[index, "lng"] = coords[municipi][1]
                dataframe.at[index, "latlng_explicit"] = 0
        # Municipi not in dictionary, fer la median amb els municipis i posant explicit a 0
        else:
            if municipi not in notInCoordNewDict:
                rowsMunicipi = dataframe.loc[dataframe['municipio'] == municipi]
                notInCoordNewDict[municipi] = (stat.median(rowsMunicipi["lat"]), stat.median(rowsMunicipi["lng"]))

            dataframe.at[index, "lat"] = notInCoordNewDict[municipi][0]
            dataframe.at[index, "lng"] = notInCoordNewDict[municipi][1]
            dataframe.at[index, "latlng_explicit"] = 0


df = pd.read_csv('fires-all.csv', index_col='id')

# Focs originats fora del territori espanyol
df.drop(df.loc[df["idmunicipio"] == 999].index, inplace=True)
df.drop(df.loc[df["idmunicipio"] == 998].index, inplace=True)

correctCoords(df)
df.to_csv('coordsCorregides.csv')
