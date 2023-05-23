import os
from dotenv import load_dotenv
from utils import *

load_dotenv()
key = os.getenv('GOOGLE_MAPS_API_KEY')

def run(path:str, output_name:str, location:str='new york'):
    load_dotenv()
    key = os.getenv('GOOGLE_MAPS_API_KEY')
    print("Running...")

    with open(path) as f:
        restaurants = [line.strip() for line in f.readlines()]
    print(f'# of Restaurants in Data: {len(restaurants)}')

    results = data_pipeline(restaurants, api_key=key, location=location)

    results.to_csv(f'./{output_name}.csv', index=False)

    print('\nFinished!')
    print(f'Data Outputted to ./{output_name}.csv')