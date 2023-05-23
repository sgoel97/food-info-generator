import os
from utils import *

load_dotenv()
key = os.getenv("GOOGLE_MAPS_API_KEY")


def run(input_path: str, output_path: str, location: str = "new york"):
    print("Running...")

    with open(input_path) as f:
        restaurants = [line.strip() for line in f.readlines()]
    print(f"# of Restaurants in Data: {len(restaurants)}")

    results = data_pipeline(restaurants, location=location)

    results.to_csv(output_path, index=False)

    print("\nFinished!")
    print(f"Data Outputted to {output_path}")
