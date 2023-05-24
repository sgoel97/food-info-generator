# Restaurant Info Generator

**Author:** [Samarth Goel](https://dev.samarthgoel.com/)

## Overview

This script takes in a list of restaurant names and a location, and outputs a csv file with a fair amount of the restaurant's data.

## Data and Setup

This script uses the Google Maps API. In order to use it, create a Google Maps API Key in the Google Cloud Console and add a `GOOGLE_MAPS_API_KEY` variable to a local `.env` file.

To use a list of restaurants as an input, put it in the `datasets` folder as a `txt` file. An example file, `nyc-bib-gourmand.txt` has been provided to demonstrate proper format. After running the script, you can find the outputted csv file in the `outputs` folder.

## Usage

After setting an API key, run `generate.ipynb` and set the `data`, `output_name`, and `location` variables at the top of the notebook and run the remaining cells. You can find the resulting csv in the `outputs` folder.

## Future Development

1. Missing Values

There's a couple of missing values, which are currently set to empty strings. Perhaps querying another search engine and cross-referencing will fix the issue.

2. Accurate Cost

While the cost column uses Google's traditional $ - $$$$ system, I want to get a more accurate cost measure in actual dollar amounts. Perhaps adding basic ML to a menu scan (given the menu can be found through the current API) or a scroll of the website to find the menu would work.
