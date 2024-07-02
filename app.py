import json
import requests
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get("visitor")
    client_ip = request.remote_addr
    response = requests.get(f"https://ipgeolocation.abstractapi.com/v1/?api_key={os.getenv('ABSTRACT_API')}&ip_address={client_ip}")
    city = response.json()['city']

    #get weather data
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.getenv('OPENWEATHER_KEY')}")
    data = json.loads(response.text)
    print(f'Data - {data}')
    temperature = data['main']['temp'] - 273.15  # Convert Kelvin to Celsius

    return jsonify({
        "client_ip": client_ip,
        "location" : city,
        "greeting": f"Hello {visitor_name}, the temperature is {temperature:.1f} degree Celcius in {city}"
        })

if __name__ == "__main__":
    app.run(debug=True)