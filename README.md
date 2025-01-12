# Weather Dashboard

A Python-based application to fetch real-time weather data for specified cities using the OpenWeather API and store it in a Google Cloud Storage bucket.

# Weather Data Collection System - DevOps Day 1 Challenge

## Features
- Fetches real-time weather data for multiple cities
- Displays temperature (°F), humidity, and weather conditions
- Automatically stores weather data a GCP bucket
- Supports multiple cities tracking
- Timestamps all data for historical tracking

---

## Technical Architecture
- **Language:** Python 3.x
- **Cloud Provider:** GCP Bucket
- **External API:** OpenWeather API
- **Dependencies:** 
  - google-cloud-storage
  - python-dotenv
  - requests

---

## Prerequisites
1. **Python 3.8+**
2. **Google Cloud Account**:
   - Set up a [GCP project](https://console.cloud.google.com/).
   - Enable the **Cloud Storage API**.
   - Create a service account and download the credentials JSON file.
3. **API Key for OpenWeather**:
   - Sign up at [OpenWeather](https://openweathermap.org/) and get your API key.

## Project Structure
weather-dashboard/
│
├── src/
│   ├── weather_dashboard.py    # Main script
│   └── ...
├── env/                        # Virtual environment
├── .env                        # Environment variables
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation

## Setup Instructions
1. Clone the repository:
```bash
git clone https://github.com/your-username/weather-dashboard.git
cd weather-dashboard

```
2. Create and Activate a Virtual Environment

```bash
python -m venv env
# On Windows:
.\env\Scripts\activate
# On macOS/Linux:
source env/bin/activate
```
3. Install dependencies:
```bash

pip install -r requirements.txt

```
4. Configure environment variables (.env):
```bash
CopyOPENWEATHER_API_KEY=your_api_key
GCP_BUCKET_NAME=your_gcp_bucket_name
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account.json
```
5. Run the application:
```bash
python src/weather_dashboard.py
```