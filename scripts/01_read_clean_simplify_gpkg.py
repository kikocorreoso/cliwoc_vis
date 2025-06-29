import datetime as dt
import json

import pandas as pd
import geopandas as gpd
import numpy as np
import antimeridian

gdf = gpd.read_file("CLIWOC21.gpkg")

################
# Some clean-up
################
# Not available hours are setted to 00:00 UTC
idx = gdf.HR.isnull()
gdf.loc[idx, "HR"] = 0
# Hours are converted to hours and minutes
gdf.loc[:, "HR"] = (gdf.loc[:, "HR"] / 100).astype(int)
gdf = gdf.rename(
    columns={
        "YR": "year",
        "MO": "month",
        "DY": "day",
        "HR": "hour",
    }
)
# invalid times
gdf["invalid_time"] = idx
# convert to datetime, not using pd.to_datetime because a strange error
datetimes = []
for i, y, m, d, h in gdf[["year", "month", "day", "hour"]].itertuples():
    datetimes.append(dt.datetime(y, m, d, int(h)))
gdf["datetimes"] = datetimes
# remove unnecesary columns
del_columns = [
    "year",
    "month",
    "day",
    "hour",
    "LON",
    "LAT",
    "TI",
    "LI",
    "DS",
    "VS",
    "NID",
    "Release",
    "TrivialCorrection",
    "IM",
    "ATTC",
    "II",
    "DI",
    "VI",
    "VV",
    "WW",
    "W1",
    "A",
    "PPP",
    "WBTI",
    "WBT",
    "DPTI",
    "DPT",
    "N",
    "NH",
    "CL",
    "HI",
    "H",
    "CM",
    "CH",
    "WD",
    "WP",
    "WH",
    "SD",
    "SP",
    "SH",
    "ATTI",
    "ATTL",
    "ATTE",
    "drLatDeg",
    "drLatMin",
    "drLatSec",
    "drLatHem",
    "drLongDeg",
    "drLongMin",
    "drLongSec",
    "drLongHem",
    "LatDeg",
    "LatMin",
    "LatSec",
    "LatHem",
    "LongDeg",
    "LongMin",
    "LongSec",
    "LongHem",
    "LatInd",
    "LonInd",
    "Calendar",
    "Year",
    "Month",
    "Day",
    "TimeOB",
    "DayOfTheWeek",
    "PartDay",
    "StartDay",
    "IT",
    "SI",
    "SST",
    "InstAbbr",
    "NumberEntry",
    "NameArchiveSet",
    "ArchivePart",
    "Specification",
    "ImageNumber",
    "Illustr",
    "DASnumber",
    "ShipSpeed",
    "CargoMemo",
    "ShipAndRigMemo",
    "BiologyMemo",
    "SSTReadingUnits",
    "BarTempReadingUnits",
    "DistUnits",
    "UnitsOfMeasurement",
    "HumidityUnits",
    "WaterAtThePumpUnits",
    "BarometerType",
    "BarometerBrand",
    "BarometerIndex",
    "HumidityMethod",
    "EstError",
    "ApplError",
    "SSTReading",
    "CurrentSpeed",
    "BarTempReading",
    "PumpWater",
    "HumReading",
    "DirClouds",
    "CloudFrac",
    "VoyageIni",
    "LMname1",
    "LMdirection1",
    "LMdistance1",
    "LMname2",
    "LMdirection2",
    "LMdistance2",
    "LMname3",
    "LMdirection3",
    "LMdistance3",
    "Watch",
    "Glasses",
    "LifeOnBoard",
    "CurrentDir",
    "EncName",
    "EncNat",
    "EncRem",
    "WarsAndFightsMemo",
    "OtherRem",
    "AnchorPlace",
    "AirThermReadingUnits",
    "AirPressureReadingUnits",
    "RefenceCourse",
    "ReferenceWindDirection",
    "Decl",
    "DistToLandmarkUnits",
    "LongitudeUnits",
    "WindScale",
    "TairReading",
    "BaroReading",
    "AllWindDirections",
    "WI",
    "Weather",
    "PrecipitationDescriptor",
]
for c in del_columns:
    del gdf[c]
# Units for some variables
gdf.loc[:, "W"] = gdf.loc[:, "W"] / 10  # Wind speed m/s
gdf.loc[:, "AT"] = gdf.loc[:, "AT"] / 10  # Air temperature ºC
gdf.loc[:, "SLP"] = gdf.loc[:, "SLP"] / 10  # Mean sea level air pressure hPa

#######################
# Create large geojson
#######################
gjson = {"type": "FeatureCollection", "features": []}
groups = gdf.groupby("ID")
for _, df in groups:
    feature = {
        "type": "Feature",
        "properties": {},
        "geometry": {
            "coordinates": [],  # list of lists each of the lists with [lon, lat]
            "type": "LineString",
        },
    }
    # unique properties: C1, InstName, InstPlace, InstLand
    # ShipName, Nationality, ShipType, Company, VoyageFrom, VoyageTo
    cols = {
        "C1": "Ship nationality",
        "InstName": "Institute name where the logbook is stored",
        "InstPlace": "Institute location where the logbook is stored",
        "InstLand": "Institute country where the logbook is stored",
        "LogbookIdent": "ID of the logbook",
        "ShipName": "Ship name",
        "Nationality": "Nationality of ship and crew",
        "ShipType": "Type of ship; e.g. schooner, barque, frigate",
        "Company": "Company",
        "VoyageFrom": "Place where the ship departed from",
        "VoyageTo": "Place where the ship sailed to",
    }
    for col, desc in cols.items():
        if (df.loc[:, col] == df[col].iloc[0]).all():
            feature["properties"][desc] = df[col].iloc[0]
    # other properties for each location:
    feature["properties"]["Wind direction (°)"] = []
    feature["properties"]["Wind speed (m/s)"] = []
    feature["properties"]["Sea level pressure (hPa)"] = []
    feature["properties"]["Air temperature (°C)"] = []
    feature["properties"]["Coastal position (near to shore)"] = []
    feature["properties"]["Master & commander (#1)"] = []
    feature["properties"]["Anchored"] = []
    feature["properties"]["Reported wind forces on this day"] = []
    feature["properties"]["Gusts present"] = []
    feature["properties"]["Rain present"] = []
    feature["properties"]["Fog present"] = []
    feature["properties"]["Snow present"] = []
    feature["properties"]["Thunder present"] = []
    feature["properties"]["Hail present"] = []
    feature["properties"]["Sea ice present"] = []
    feature["properties"]["Date and time (UTC)"] = []
    for t in df.itertuples():
        if pd.notnull([t.longitude, t.latitude, t.datetimes]).all():
            feature["geometry"]["coordinates"].append([t.longitude, t.latitude])
            if t.invalid_time:
                time = "Unknown"
            else:
                time = t.datetimes.strftime("%H:%M")
            feature["properties"]["Date and time (UTC)"].append(
                f"{t.datetimes.strftime('%Y/%m/%d')} {time}"
            )
            if pd.notnull(t.D):
                feature["properties"]["Wind direction (°)"].append(int(t.D))
            else:
                feature["properties"]["Wind direction (°)"].append("N/A")
            if pd.notnull(t.W):
                feature["properties"]["Wind speed (m/s)"].append(t.W)
            else:
                feature["properties"]["Wind speed (m/s)"].append("N/A")
            if pd.notnull(t.SLP):
                feature["properties"]["Sea level pressure (hPa)"].append(t.SLP)
            else:
                feature["properties"]["Sea level pressure (hPa)"].append("N/A")
            if pd.notnull(t.AT):
                feature["properties"]["Air temperature (°C)"].append(t.AT)
            else:
                feature["properties"]["Air temperature (°C)"].append("N/A")
            if pd.notnull(t.PosCoastal):
                feature["properties"][
                    "Coastal position (near to shore)"
                ].append(int(t.PosCoastal))
            else:
                feature["properties"][
                    "Coastal position (near to shore)"
                ].append("N/A")
            if pd.notnull([t.Name1, t.Rank1]).all():
                feature["properties"]["Master & commander (#1)"].append(
                    f"{t.Rank1} {t.Name1}"
                )
            else:
                feature["properties"]["Master & commander (#1)"].append(
                    "Unknown"
                )
            if pd.notnull(t.Anchored):
                feature["properties"]["Anchored"].append(int(t.Anchored))
            else:
                feature["properties"]["Anchored"].append("N/A")
            if pd.notnull(t.AllWindForces):
                try:
                    value = int(t.AllWindForces)
                except:
                    value = t.AllWindForces
                feature["properties"][
                    "Reported wind forces on this day"
                ].append(value)
            else:
                feature["properties"][
                    "Reported wind forces on this day"
                ].append("N/A")
            if pd.notnull(t.Gusts):
                feature["properties"]["Gusts present"].append(int(t.Gusts))
            else:
                feature["properties"]["Gusts present"].append("N/A")
            if pd.notnull(t.Rain):
                feature["properties"]["Rain present"].append(int(t.Rain))
            else:
                feature["properties"]["Rain present"].append("N/A")
            if pd.notnull(t.Fog):
                feature["properties"]["Fog present"].append(int(t.Fog))
            else:
                feature["properties"]["Fog present"].append("N/A")
            if pd.notnull(t.Snow):
                feature["properties"]["Snow present"].append(int(t.Snow))
            else:
                feature["properties"]["Snow present"].append("N/A")
            if pd.notnull(t.Thunder):
                feature["properties"]["Thunder present"].append(int(t.Thunder))
            else:
                feature["properties"]["Thunder present"].append("N/A")
            if pd.notnull(t.Hail):
                feature["properties"]["Hail present"].append(int(t.Hail))
            else:
                feature["properties"]["Hail present"].append("N/A")
            if pd.notnull(t.SeaIce):
                feature["properties"]["Sea ice present"].append(int(t.SeaIce))
            else:
                feature["properties"]["Sea ice present"].append("N/A")
    # If all coordinates are invalid then avoid this record.
    # If only one location for a linestring then avoid this record.
    if len(feature["geometry"]["coordinates"]) > 1:
        gjson["features"].append(feature)
    # Remove unnecesary noise if information is not useful.
    # Lower geojson size
    cols = [
        "Wind direction (°)",
        "Wind speed (m/s)",
        "Sea level pressure (hPa)",
        "Air temperature (°C)",
        "Coastal position (near to shore)",
        "Master & commander (#1)",
        "Anchored",
        "Reported wind forces on this day",
        "Gusts present",
        "Rain present",
        "Fog present",
        "Snow present",
        "Thunder present",
        "Hail present",
        "Sea ice present",
        "Date and time (UTC)",
    ]
    for col in cols:
        data = feature["properties"][col]
        if all(x == data[0] for x in data):
            try:
                feature["properties"][col] = data[0]
            except:
                pass  # No data

gjson = antimeridian.fix_geojson(gjson)

with open("cliwoc1.json", "w") as f:
    json.dump(gjson, f)
