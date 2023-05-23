import os
import requests
from typing import List
from tqdm import tqdm
from dotenv import load_dotenv
from yelpapi import YelpAPI
import pandas as pd
import numpy as np


def get_restaurant_id(name: str, location: str, google_api_key: str):
    inputtype = "textquery"
    fields = ["name", "place_id"]

    name = name + " " + location
    name = name.replace(" ", "%20")
    fields = "%2C".join(fields)

    payload = {}
    headers = {}

    try:
        url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={name}&inputtype={inputtype}&fields={fields}&key={google_api_key}"
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()
        place_id = data["candidates"][0]["place_id"]

    except:
        name = name + " " + location + " restaurant"
        url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={name}&inputtype={inputtype}&fields={fields}&key={google_api_key}"
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()
        place_id = data["candidates"][0]["place_id"]

    return place_id


def get_info_from_id(
    name: str, place_id: str, location: str, google_api_key: str, yelp_api_key: str
):
    fields = ["name", "rating", "address_components", "website", "price_level"]
    fields = "%2C".join(fields)

    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields={fields}&key={google_api_key}"
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()

    if not data["result"]:
        print(name, data)
        return

    result = data["result"]
    result["found_name"] = result["name"]
    result["name"] = name
    result["address_components"] = list(
        filter(
            lambda x: "locality" in x["types"] or "sublocality_level_1" in x["types"],
            result["address_components"],
        )
    )
    result["address_components"] = result["address_components"][0]["short_name"]

    with YelpAPI(yelp_api_key) as yelp_api:
        search_results = yelp_api.search_query(
            term=name, location=f'{result["address_components"]}, {location}', limit=1
        )
    try:
        restaurant_data = search_results["businesses"][0]
        result["cuisine"] = ", ".join(
            list(map(lambda x: x["title"], restaurant_data["categories"]))
        )
        result["yelp_rating"] = restaurant_data["rating"]
        if "price_level" not in result:
            result["price_level"] = restaurant_data["price"]
    except:
        pass

    return result


def data_pipeline(restaurant_list: List[str], location: str):
    load_dotenv()
    google_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    yelp_api_key = os.getenv("YELP_API_KEY")
    data = []

    for restaurant in tqdm(restaurant_list):
        place_id = get_restaurant_id(restaurant, location, google_api_key)
        restaurant_data = get_info_from_id(
            restaurant, place_id, location, google_api_key, yelp_api_key
        )
        data.append(restaurant_data)

    start_cols = [
        "name",
        "found_name",
        "website",
        "cuisine",
        "rating",
        "yelp_rating",
        "price_level",
        "address_components",
    ]
    end_cols = [
        "Name",
        "Found Name",
        "Website",
        "Cuisine",
        "Location",
        "Cost",
        "Notes",
        "Google Rating",
        "Yelp Rating",
    ]
    df = pd.DataFrame(data, columns=start_cols)
    df["price_level"] = df["price_level"].replace(
        {1: "$", 2: "$$", 3: "$$$", 4: "$$$$"}
    )
    df["Notes"] = np.array([""] * len(df))
    df = df.replace(np.nan, "")
    df = df.rename(
        columns={
            "name": "Name",
            "found_name": "Found Name",
            "cuisine": "Cuisine",
            "website": "Website",
            "rating": "Google Rating",
            "yelp_rating": "Yelp Rating",
            "address_components": "Location",
            "price_level": "Cost",
        }
    )

    df = df[end_cols]

    return df
