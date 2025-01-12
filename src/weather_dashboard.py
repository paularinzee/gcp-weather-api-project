import os
import json
import requests
from datetime import datetime
from google.cloud import storage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
print("OpenWeather API Key:", os.getenv('OPENWEATHER_API_KEY'))
print("GCP Bucket Name:", os.getenv('GCP_BUCKET_NAME'))
print("GCP Credentials Path:", os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
class WeatherDashboard:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.bucket_name = os.getenv('GCP_BUCKET_NAME')
        self.gcs_client = storage.Client()

    def create_bucket_if_not_exists(self):
        """Create GCS bucket if it doesn't exist"""
        try:
            bucket = self.gcs_client.lookup_bucket(self.bucket_name)
            if bucket:
                print(f"Bucket {self.bucket_name} exists")
            else:
                print(f"Creating bucket {self.bucket_name}")
                self.gcs_client.create_bucket(self.bucket_name)
                print(f"Successfully created bucket {self.bucket_name}")
        except Exception as e:
            print(f"Error checking/creating bucket: {e}")

    def fetch_weather(self, city):
        """Fetch weather data from OpenWeather API"""
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "imperial"
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def save_to_gcs(self, weather_data, city):
        """Save weather data to GCS bucket"""
        if not weather_data:
            return False
            
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        file_name = f"weather-data/{city}-{timestamp}.json"
        
        try:
            bucket = self.gcs_client.get_bucket(self.bucket_name)
            blob = bucket.blob(file_name)
            
            weather_data['timestamp'] = timestamp
            blob.upload_from_string(
                data=json.dumps(weather_data),
                content_type='application/json'
            )
            print(f"Successfully saved data for {city} to GCS")
            return True
        except Exception as e:
            print(f"Error saving to GCS: {e}")
            return False

def main():
    dashboard = WeatherDashboard()
    
    # Create bucket if needed
    dashboard.create_bucket_if_not_exists()
    
    cities = ["Philadelphia", "Seattle", "New York"]
    
    for city in cities:
        print(f"\nFetching weather for {city}...")
        weather_data = dashboard.fetch_weather(city)
        if weather_data:
            temp = weather_data['main']['temp']
            feels_like = weather_data['main']['feels_like']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']
            
            print(f"Temperature: {temp}°F")
            print(f"Feels like: {feels_like}°F")
            print(f"Humidity: {humidity}%")
            print(f"Conditions: {description}")
            
            # Save to GCS
            success = dashboard.save_to_gcs(weather_data, city)
            if success:
                print(f"Weather data for {city} saved to GCS!")
        else:
            print(f"Failed to fetch weather data for {city}")

if __name__ == "__main__":
    main()
