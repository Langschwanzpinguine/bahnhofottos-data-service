import json
from config import country_codes_file, countries_interest_file, data_directory


def get_all_names():
    input_json_file_path = f'{data_directory}/train_station_data.json'
    output_json_file_path = f'{data_directory}/all_names.json'


    with open(input_json_file_path, 'r') as input_file:
        data = json.load(input_file)

    if 'elements' in data:
        stations = []
        for element in data['elements']:
            if 'id' in element and 'tags' in element:
                station_data = {
                    'id': element['id'],
                    'name': element['tags'].get('name', 'N/A')
                }
                stations.append(station_data)
        output_data = {'stations': stations}

        with open(output_json_file_path, 'w') as output_file:
            json.dump(output_data, output_file, indent=2)
    else:
        print('The "elements" key does not exist in the JSON data.')

    print(f'New JSON data saved to {output_json_file_path}')

def get_unique_names():
    input_json_file_path = f'{data_directory}/train_station_data.json'
    output_json_file_path = f'{data_directory}/unique_names.json'

    with open(input_json_file_path, 'r') as input_file:
        data = json.load(input_file)

    if 'elements' in data:
        stations = []
        unique_names = set()
        for element in data['elements']:
            if 'id' in element and 'tags' in element:
                name = element['tags'].get('name', 'N/A')
                if name not in unique_names:
                    station_data = {
                        'id': element['id'],
                        'name': name
                    }
                    stations.append(station_data)
                    unique_names.add(name)

        output_data = {'stations': stations}

        with open(output_json_file_path, 'w') as output_file:
            json.dump(output_data, output_file, indent=2)
    else:
        print('The "elements" key does not exist in the JSON data.')

    print(f'New JSON data saved to {output_json_file_path}')