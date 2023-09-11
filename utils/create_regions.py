import json
import requests
from config import *

def create_regions():
    with open(country_info, 'r', encoding='utf-8') as file:
        countries_data = json.load(file)

    with open(country_codes_file, 'r', encoding='utf-8') as file:
        flags_data = json.load(file)

    country_flags = {country["code"]: country["flag"] for country in flags_data["countries"]}

    countries_by_subregion = {}

    for country in countries_data['countries']:
        subregion = country.get("Sub-region Name", "Other")  # Use "Other" if subregion is missing
        if subregion not in countries_by_subregion:
            countries_by_subregion[subregion] = []

        country_code = country["ISO3166-1-Alpha-2"]
        flag = country_flags.get(country_code, "🏳️")  # Use a default flag emoji if not found

        country_stuff = {
            "name": country["CLDR display name"],
            "country_code": country_code,
            "flag": flag
        }
        countries_by_subregion[subregion].append(country_stuff)

    with open(f"{persistent_data}/grouped_countries.json", 'w', encoding='utf-8') as file:
        json.dump(countries_by_subregion, file, ensure_ascii=False, indent=4)

def add_flags_to_countries():
    with open(country_info, 'r', encoding='utf-8') as file:
        country_info_data = json.load(file)

    with open(country_codes_file, 'r', encoding='utf-8') as file:
        flags_data = json.load(file)

    country_flags = {country["code"]: country["flag"] for country in flags_data["countries"]}

    for country in country_info_data['countries']:
        country_code = country.get("ISO3166-1-Alpha-2", "")
        flag = country_flags.get(country_code, "")
        country["flag"] = flag

    with open(country_info, 'w', encoding='utf-8') as file:
        json.dump(country_info_data, file, ensure_ascii=False, indent=4)


def add_bounding_box_to_countries():
    print("Started fetching bounding boxes")
    with open(country_info, 'r', encoding='utf-8') as file:
        country_info_data = json.load(file)
    print('Loaded file')
    country_bounding_boxes = {}

    for country in country_info_data["countries"]:
        country_name = country.get("CLDR display name").replace("&", "and")
        print(f'Starting to fetch {country_name}')
        query_url = f"https://nominatim.openstreetmap.org/search?q={country_name}&format=json"
        
        try:
            response = requests.get(query_url)
            response.raise_for_status()
            data = response.json()
            print(f'Response to json')
            if data and isinstance(data, list):
                first_result = data[0]
                bounding_box = first_result.get("boundingbox", [])
                print(f'Response is list')
                if len(bounding_box) == 4:
                    print(bounding_box)
                    # Store the bounding box coordinates as a list of floats
                    bounding_box = [float(coord) for coord in bounding_box]
                    country_bounding_boxes[country_name] = bounding_box
                    print(f'Saved bbox of {country_name}')
        except Exception as e:
            print(f"Error fetching bounding box for {country_name}: {str(e)}")

    # Add bounding boxes to the existing country info

    print(f'Adding to existing data')
    for country in country_info_data['countries']:
        country_name = country.get('CLDR display name').replace("&", "and")
        bounding_box = country_bounding_boxes.get(country_name, [])
        print(bounding_box)
        country["bounding_box"] = bounding_box
    print(f'Writing data to file')
    with open(country_info, 'w', encoding='utf-8') as file:
        json.dump(country_info_data, file, ensure_ascii=False, indent=4)

def create_ultimate_dataset():
     # Read the existing JSON file
    with open(country_info, 'r', encoding='utf-8') as file:
        data = json.load(file)

    transformed_data = {"countries": []}

    for country in data["countries"]:
        transformed_country = {
            "name": country["CLDR display name"],
            "flag": country.get("flag", ""),
            "code": country["ISO3166-1-Alpha-2"],
            "bounding_box": country.get("bounding_box", []),
            "continent": country["Continent"],
            "sub-region name": country.get("Sub-region Name", "")
        }
        transformed_data["countries"].append(transformed_country)

    # Write the transformed data to a new JSON file
    with open(compiled_info, 'w', encoding='utf-8') as file:
        json.dump(transformed_data, file, ensure_ascii=False, indent=4)
