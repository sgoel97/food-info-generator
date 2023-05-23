import requests
from typing import List
from tqdm import tqdm
import pandas as pd
import numpy as np

def get_restaurant_id(name:str, api_key:str, location:str):
    inputtype = "textquery"
    fields = ['name', 'place_id']
    
    name = name + ' ' + location
    name = name.replace(" ", "%20")
    fields = '%2C'.join(fields)

    payload={}
    headers = {}
    try:
        url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={name}&inputtype={inputtype}&fields={fields}&key={api_key}"
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()
        place_id = data['candidates'][0]['place_id']

    except:
        name = name + ' ' + location + ' restaurant'
        url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={name}&inputtype={inputtype}&fields={fields}&key={api_key}"
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()
        place_id = data['candidates'][0]['place_id']

    return place_id

def get_info_from_id(place_id:str, api_key:str):
    fields = ['name', 'rating', 'address_components', 'website', 'price_level']
    fields = '%2C'.join(fields)

    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields={fields}&key={api_key}"
    payload={}
    headers = {}
    
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    try:
        result = data['result']
        result['address_components'] = list(filter(lambda x: "locality" in x['types'] or 'sublocality_level_1' in x['types'], result['address_components']))
        result['address_components'] = result['address_components'][0]['short_name']
        result

        return result
    except:
        print(data)

def data_pipeline(restaurant_list:List[str], api_key:str, location:str):
    data = []

    for restaurant in tqdm(restaurant_list):
        place_id = get_restaurant_id(restaurant, api_key, location)
        restaurant_data = get_info_from_id(place_id, api_key)
        data.append(restaurant_data)
    
    start_cols = ['name', 'website', 'rating', 'price_level', 'address_components']
    end_cols=["Name","Website","Cuisine","Google Rating","Location","Cost","Notes"]
    df = pd.DataFrame(data, columns=start_cols)
    df['price_level'] = df['price_level'].map({1: '$', 2: '$$', 3: '$$$', 4: '$$$$'})
    df['Cuisine'] = np.array([''] * len(df))
    df['Notes'] = np.array([''] * len(df))
    df = df.replace(np.nan, '')
    df = df.rename(columns=
        {
            'name': 'Name', 
            'website': "Website", 
            'rating': 'Google Rating', 
            'address_components': 'Location',
            'price_level': 'Cost'
        }
    )

    df = df[end_cols]

    return df