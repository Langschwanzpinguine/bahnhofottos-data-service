import json
import requests
from config import country_codes_file, countries_interest_file, data_directory

def update_total_data():
    print("Updating total train station data")
    overpass_body = f'''
        [out:json][timeout:600];
        (node["railway"="station"];node["railway"="halt"];);out center;
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
            file_name = f'{data_directory}/train_station_data.json'
            with open(file_name, 'w') as json_file:
                json.dump(json_data, json_file, indent=4)
                print(f'Response data saved to {file_name}')
    else:
        print('POST request failed with status code:', response.status_code)
        print('Response:', response.text)