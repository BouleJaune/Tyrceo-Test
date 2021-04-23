import pymysql
import pandas as pd
from mapbox import Geocoder
from shapely.geometry import Point

import geopandas as gpd

""""
COMMMENTED BECAUSE I SAVED THE DATA INTO CSV FILES
connection = pymysql.connect(host="34.77.194.159", user="candidate", database="Hiring_task", password="Fbps9Y7MhKQa4XPxjYo8")
query_hotel_info = "SELECT * FROM hotel_info WHERE country_area IN ('Madrid', 'Barcelona', 'Costa del Sol', 'Costa Blanca')"
h_info_df = pd.read_sql(query_hotel_info, connection)
h_info_df.to_csv("data.csv")


query_reviews = "SELECT * FROM hotel_reviews WHERE year(review_date) in (2018, 2019)"
h_reviews_df = pd.read_sql(query_reviews, connection)
h_reviews_df.to_csv("hotel_reviews.csv")
"""

#load from csv the different df
h_info_df = pd.read_csv("hotel_info.csv")
h_reviews_df = pd.read_csv("hotel_reviews.csv")

#Remove unwanted column
h_info_df = h_info_df.drop("Unnamed: 0", axis=1) 
h_reviews_df = h_reviews_df.drop("Unnamed: 0", axis=1) 

#Remove review if the corresponding hotel has less than 5 reviews in 2019
h_reviews_df = h_reviews_df[h_reviews_df["review_date"]>="2019-01-01"].groupby("hotel_id").filter(lambda x: len(x)>=5) 
#Create df of hotel_id to keep 
hotel_id_tokeep =  h_reviews_df.drop_duplicates(subset=["hotel_id"])["hotel_id"] 

#Filter the hotel_info df
h_info_df = h_info_df[ h_info_df["hotel_id"].isin(hotel_id_tokeep)] 

#remove from memory now-pointless dfs
del hotel_id_tokeep
del h_reviews_df

"""I geocode with mapbox however it doesn't seem to be such a good idea. Anyway most of the solution are paid one so..."""
mapbox_access_token = "pk.eyJ1Ijoiam1jYXJyYXNjb3NhIiwiYSI6ImNrZGlvcmIzMzA3MW0zMG50dG90NWJ0aTEifQ.ZoobdVV5OqJUUVH-k2ZHDg"
geocoder = Geocoder(access_token=mapbox_access_token)

def geocode_address(address):
    response = geocoder.forward(address)
    coords = str(response.json()['features'][0]['center'])
    coords = coords.replace(']', '')
    coords = coords.replace('[', '')
    return coords


def geocode_df(row):
    coords = geocode_address(row["hotel_address"])
    lat, lng = coords.split(", ")
    lat = float(lat)
    lng = float(lng)
    return lat, lng

latlong = h_info_df.apply(geocode_df, axis=1) 
h_info_df["geolocation"] = latlong.apply(Point)
gdf = gpd.GeoDataFrame(h_info_df, geometry="geolocation")

gdf.to_file("hotel.geojson", driver='GeoJSON')
