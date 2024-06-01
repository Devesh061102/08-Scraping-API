from flask import Flask, render_template, jsonify, request
import os
import pandas as pd
import requests

app = Flask(__name__)

@app.route('/')
def home():
    """
    Render the homepage with instructions and a list of cities.
    """
    return render_template('index.html')

@app.route('/weather', methods=['GET'])
def get_weather():
    """
    Fetch weather data from OpenWeatherMap API and save it to a CSV file.
    """
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City not provided'}), 400

    zip_codes = {
    'Delhi': '110001',
    'Mumbai': '400001',
    'Kolkata': '700001',
    'Chennai': '600001',
    'Bangalore': '560001',
    'Hyderabad': '500001',
    'Pune': '411001',
    'Ahmedabad': '380001',
    'Jaipur': '302001',
    'Lucknow': '226001',
    'Surat': '395001',
    'Kanpur': '208001',
    'Nagpur': '440001',
    'Indore': '452001',
    'Thane': '400601',
    'Bhopal': '462001',
    'Visakhapatnam': '530001',
    'Pimpri': '411018',
    'Patna': '800001',
    'Vadodara': '390001',
    'Ghaziabad': '201001',
    'Ludhiana': '141001',
    'Agra': '282001',
    'Nashik': '422001',
    'Faridabad': '121001',
    'Meerut': '250001',
    'Rajkot': '360001',
    'Kalyan': '421301',
    'Vasai': '401201',
    'Varanasi': '221001'
}

    if city not in zip_codes:
        return jsonify({'error': 'Invalid city'}), 400

    zip_code = zip_codes[city]
    api_key = 'Key'  # Replace with your actual API key

    geocode_url = f'http://api.openweathermap.org/geo/1.0/zip?zip={zip_code},IN&appid={api_key}'
    geocode_response = requests.get(geocode_url)

    if geocode_response.status_code != 200:
        return jsonify({'error': 'Could not fetch geocode data'}), geocode_response.status_code

    geocode_data = geocode_response.json()
    lat = geocode_data['lat']
    lon = geocode_data['lon']

    weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
    weather_response = requests.get(weather_url)

    if weather_response.status_code != 200:
        return jsonify({'error': 'Could not fetch weather data'}), weather_response.status_code

    weather_data = weather_response.json()

    temperature = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    description = weather_data['weather'][0]['description']
    timestamp = pd.Timestamp.now()

    weather_info = {
        'city': city,
        'latitude': lat,
        'longitude': lon,
        'temperature': temperature,
        'humidity': humidity,
        'description': description,
        'timestamp': timestamp
    }
    weather_info_df = pd.DataFrame([weather_info])

    # Check if weather_data.csv exists, if not, create an empty DataFrame
    if not os.path.exists('weather_data.csv'):
        df = pd.DataFrame(columns=['city', 'latitude', 'longitude', 'temperature', 'humidity', 'description', 'timestamp'])
    else:
        # Load existing weather data from CSV
        df = pd.read_csv('weather_data.csv')

    # Update existing entry or add new one
    if not df.empty and city in df['city'].values:
        df.loc[df['city'] == city, ['latitude', 'longitude', 'temperature', 'humidity', 'description', 'timestamp']] = \
            [lat, lon, temperature, humidity, description, timestamp]
    else:
        df = pd.concat([df, weather_info_df], ignore_index=True)

    # Save to CSV
    df.to_csv('weather_data.csv', index=False)

    return jsonify({'message': 'Weather data fetched and stored successfully'}), 200

@app.route('/weather_data', methods=['GET'])
def get_weather_data():
    """
    Retrieve stored weather data and display it as a DataFrame.
    """
    if os.path.exists('weather_data.csv'):
        stored_data = pd.read_csv('weather_data.csv')
        return render_template('weather_data.html', data=stored_data.to_dict(orient='records'))
    else:
        return jsonify({'error': 'No weather data found'}), 404

if __name__ == '__main__':
    app.run(debug=True)


### Part 2: Creating Your Own API ###

# @app.route('/jobs', methods=['GET'])
# def get_jobs():
#     """
#     Endpoint to fetch all jobs data.
#     """
#     return jobs_df.to_json(orient='records')

# @app.route('/jobs/<int:job_id>', methods=['GET'])
# def get_job(job_id):
#     """
#     Endpoint to fetch a specific job by ID.
#     """
#     if 0 <= job_id < len(jobs_df):
#         job = jobs_df.iloc[job_id].to_dict()
#         return jsonify(job)
#     else:
#         return jsonify({'error': 'Job not found'}), 404

# if __name__ == "__main__":
#     app.run(debug=True)
