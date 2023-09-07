from flask import Flask, request, jsonify
from utils.refresh_countries import *

app = Flask(__name__)

@app.route('/refresh/all', methods=['POST'])
def refresh_all():
    print("refresh all")
    return '', 204

@app.route('/refresh/countries', methods=['POST']) # Expects a json body like {"countries" : ["CH", "DE"]}
def refresh_countries():
    try:
        data = request.get_json()
        if 'countries' in data:
            countries = data['countries']
            update_countries_from_list(countries)
            return '', 204
        else:
            return jsonify({"error": "Missing 'countries' in JSON body"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/refresh/all_countries', methods=['POST'])
def refresh_all_countries():
    update_countries()
    return '', 204

@app.route('/add_countries', methods=['POST']) #{"countries": ["AT"], refresh_now: boolean}
def add_countries():
    try:
        data = request.get_json()
        if 'countries' in data:
            countries = data['countries']
            add_countries_to_list(countries)

            if('refresh_now') in data and data['refresh_now']:
                update_countries_from_list(countries)

            return '', 204
        else:
            return jsonify({"error": "Missing 'countries' in JSON body"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete_countries', methods=['POST'])
def delete_countries():
    try:
        data = request.get_json()
        if 'countries' in data:
            countries = data['countries']
            delete_countries_from_list(countries)
            return '', 204
        else:
            return jsonify({"error": "Missing 'countries' in JSON body"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="localhost", port=8080)