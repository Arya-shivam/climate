from flask import Flask, render_template, jsonify, url_for
import requests
import json
import random
import datetime
#from config import API_KEY, API_URL  # Assume API key and URL are defined in config.py

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    image_url = url_for('static', filename='planetary_climate.jpg')
    print(f"Image URL: {image_url}")  # This will print in your console
    climate_monitoring = {
        'monthly_reports': {
            'title': 'Monthly Climate Reports',
            'description': 'Access our comprehensive monthly climate reports, with analyses of global climate patterns, temperature trends, and precipitation data.',
            'image': 'monthly_report.jpg'
        },
        'climate_glance': {
            'title': 'Climate at a Glance',
            'description': 'Get a quick overview of key climate indicators and trends. Our "Climate at a Glance" feature offers easy-to-understand visualizations.',
            'image': 'climate_glance.jpg'
        },
        'billion_dollar_disasters': {
            'title': 'Billion-Dollar Disasters',
            'description': 'Track the increasing frequency and cost of extreme weather events. Our Billion-Dollar Disasters tracker provides detailed information on major climate events.',
            'image': 'disasters.jpg'
        },
        'climate_change_indicators': {
            'title': 'Climate Change Indicators',
            'description': 'Explore key indicators of climate change, including sea level rise, ocean heat content, and Arctic sea ice extent.',
            'image': 'indicators.jpg'
        }
    }
    
    other_products = [
        {
            'name': 'Climate Data Online',
            'description': 'Access and download climate data from our extensive online database.',
            'graph_data': json.dumps([random.randint(20, 30) for _ in range(12)]),
            'link': '/climate-data-online'
        },
        {
            'name': 'Storm Events Database',
            'description': 'Explore detailed information about storm events across the globe.',
            'graph_data': json.dumps([random.randint(5, 15) for _ in range(12)]),
            'link': '/storm-events-database'
        },
        {
            'name': 'Global Historical Climatology Network',
            'description': 'Analyze historical climate data from thousands of weather stations worldwide.',
            'graph_data': json.dumps([random.randint(10, 20) for _ in range(12)]),
            'link': '/global-historical-climatology-network'
        },
        {
            'name': 'Drought Monitoring',
            'description': 'Stay informed about drought conditions and their impacts on different regions.',
            'graph_data': json.dumps([random.randint(0, 10) for _ in range(12)]),
            'link': '/drought-monitoring'
        },
        {
            'name': 'Satellite Data',
            'description': 'Access a wide range of satellite-derived climate and weather data products.',
            'graph_data': json.dumps([random.randint(15, 25) for _ in range(12)]),
            'link': '/satellite-data'
        },
        {
            'name': 'Paleoclimatology Data',
            'description': 'Explore climate data from the distant past to understand long-term trends.',
            'graph_data': json.dumps([random.randint(5, 15) for _ in range(12)]),
            'link': '/paleoclimatology-data'
        }
    ]
    
    featured_news = [
        {
            'title': 'Climate Research Update',
            'description': 'Latest findings in climate modeling and predictions...',
            'image': 'news1.jpg'
        },
        {
            'title': 'New Data Sources Added',
            'description': 'Expanding our database with recent satellite observations...',
            'image': 'news2.jpg'
        },
        {
            'title': 'Upcoming Climate Conference',
            'description': 'Join us for the annual Climate Modeling Symposium...',
            'image': 'news3.jpg'
        }
    ]
    
    return render_template('home.html', climate_monitoring=climate_monitoring, other_products=other_products, featured_news=featured_news)

# Monthly Report Page
@app.route('/monthly-report')
def monthly_report_page():
    return render_template('monthly_report.html')  # Renders the monthly report page

# API Endpoint for Monthly Climate Data
#@app.route('/api/monthly-climate-data', methods=["GET"])
#def get_monthly_climate_data():
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=30)
    
    # Example API request for climate data (replace with actual API URL)
    response = requests.get(f"{API_URL}/climate?start_date={start_date}&end_date={today}&apikey={API_KEY}")
    
    if response.status_code == 200:
        data = response.json()
        # Processing data as needed for the frontend
        processed_data = [
            {
                "date": entry["date"],
                "temperature": entry["temperature"],
                "humidity": entry["humidity"],
                "precipitation": entry["precipitation"]
            }
            for entry in data["results"]
        ]
        return jsonify(processed_data)
    else:
        return jsonify({"error": "Failed to fetch data"}), 500

# Other routes for additional pages
@app.route('/climate-data-online')
def climate_data_online():
    return "Climate Data Online Page"

@app.route('/storm-events-database')
def storm_events_database():
    return "Storm Events Database Page"

@app.route('/global-historical-climatology-network')
def global_historical_climatology_network():
    return "Global Historical Climatology Network Page"

@app.route('/drought-monitoring')
def drought_monitoring():
    return "Drought Monitoring Page"

@app.route('/satellite-data')
def satellite_data():
    return "Satellite Data Page"

@app.route('/paleoclimatology-data')
def paleoclimatology_data():
    return "Paleoclimatology Data Page"

if __name__ == '__main__':
    app.run(debug=True)
