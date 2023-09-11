import json
import requests
import os
import time
from config import country_codes_file, countries_interest_file, data_directory

def is_valid_country_code(country_code):
    try:
        with open(country_codes_file, 'r') as file:
            data = json.load(file)
            countries = data.get('countries', [])
            for country in countries:
                if 'Code' in country and country['Code'] == country_code:
                    return True
        return False
    except FileNotFoundError:
        return False

def update_country(country): #Assumes correct code
    print("Updating " + country)
    overpass_body = f'''
        [out:json][timeout:360];
        area["ISO3166-1"="{country}"][admin_level=2];
        (
            node
                [railway=station]
                (area);
        );
        out;

        area["ISO3166-1"="{country}"][admin_level=2];
        (
            node
                [railway=halt]
                (area);
            );
        out;
    '''

    url = "https://overpass-api.de/api/interpreter"
    headers = {'Content-Type': 'text/plain'}

    response = requests.post(url, data=overpass_body, headers=headers)

    if response.status_code == 200:
        try:
            json_data = json.loads(response.text)
        except json.JSONDecodeError as e:
            print('Error decoding JSON response:', str(e))
            json_data = None
        
        if json_data:
            file_name = f'{data_directory}/country_data_{country}.json'
            with open(file_name, 'w') as json_file:
                json.dump(json_data, json_file, indent=4)
                print(f'Response data saved to {file_name}')
    else:
        print('POST request failed with status code:', response.status_code)
        print('Response:', response.text)
    
    return response

def update_countries_from_list(country_list):
    unique_countries = list(set(country_list))

    for country in unique_countries:
        if not is_valid_country_code(country):
            print(country + " is not a valid ISO 3166-1 country code")
            continue
        update_country(country)
        time.sleep(10)
   

def update_countries():
    input_json_file_path = countries_interest_file

    if not os.path.exists(input_json_file_path):
        return

    with open(input_json_file_path, 'r') as input_file:
        data = json.load(input_file)

    if 'countries' in data:
        update_countries_from_list(data['countries'])
    else:
        print('The "countries" key does not exist in the JSON data.')

def add_countries_to_list(countries):
    print("GOT HERE")
    if not os.path.exists(countries_interest_file):
        initial_data = {'countries': []}
        print("GOT HERE")
        with open(countries_interest_file, 'w') as new_file:
            json.dump(initial_data, new_file, indent=4)
        print(f'File {countries_interest_file} was created.')
    print("GOT HERE")

    try:
        with open(countries_interest_file, 'r') as file:
            data = json.load(file)
            existing_countries = data.get('countries', [])
        
        for country_code in countries:
            if not is_valid_country_code(country_code):
                print(country_code + " is not a valid ISO 3166-1 country code")
                continue
            if country_code not in existing_countries:
                existing_countries.append(country_code)

        data['countries'] = existing_countries
        
        with open(countries_interest_file, 'w') as file:
            json.dump(data, file, indent=4)
        
        return "Countries added successfully"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def delete_countries_from_list(countries_to_remove):
    try:
        with open(countries_interest_file, 'r') as file:
            data = json.load(file)
            existing_countries = data.get('countries', [])

        updated_countries = [country for country in existing_countries if country not in countries_to_remove]

        data['countries'] = updated_countries

        with open(countries_interest_file, 'w') as file:
            json.dump(data, file, indent=4)

        files_to_delete = []
        for country_code in countries_to_remove:
            filename = f'{data_directory}/country_data_{country_code}.json'
            print(filename)
            files_to_delete.append(filename)
            print(files_to_delete)
            if os.path.exists(filename):
                os.remove(filename)

        return "Countries removed successfully"
    except FileNotFoundError:
        return "countries_of_interest not found"
    except Exception as e:
        return f"An error occurred: {str(e)}"
