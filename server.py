from flask import Flask, request, jsonify
from utils.refresh_countries import update_countries

app = Flask(__name__)

@app.route('/refresh/all', methods=['POST'])
def refresh_all():
    print("refresh all")
    return '', 204

@app.route('/refresh/countries', methods=['POST'])
def refresh_countries():
    print("Refresh country")
    return '', 204

@app.route('/refresh/all_countries', methods=['POST'])
def refresh_all_countries():
    update_countries()
    return '', 204

@app.route('/add_countries', methods=['POST'])
def add_country():
    update_countries()

    return '', 204
    # For each country run refresh

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="localhost", port=8080)