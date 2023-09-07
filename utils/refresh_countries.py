import json
import requests

def update_country(country):
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
            file_name = f'data/country_data_{country}.json'
            with open(file_name, 'w') as json_file:
                json.dump(json_data, json_file, indent=4)
                print(f'Response data saved to {file_name}')
    else:
        print('POST request failed with status code:', response.status_code)
        print('Response:', response.text)


def update_countries():
    input_json_file_path = 'data/countries_of_interest.json'
    output_json_file_path = 'data/data_{{country}}.json'

    with open(input_json_file_path, 'r') as input_file:
        data = json.load(input_file)

    if 'countries' in data:
        for country in data['countries']:
            update_country(country)

    else:
        print('The "countries" key does not exist in the JSON data.')