import os
import requests
import pandas as pd
import argparse
from dotenv import load_dotenv
import time

class APILimitExceeded(Exception):
    pass

def get_api_key(provided_key=None):
    if provided_key:
        return provided_key
    
    load_dotenv()
    api_key = os.getenv('API_KEY')
    
    if not api_key:
        raise ValueError("API_KEY not found. Please provide it as an argument or set it in your environment variables.")
    
    return api_key

def fetch_sensor_data(api_key):
    API_LIST_SENSORS_URL = "https://api.breathelondon.org/api/ListSensors"
    
    start_time = time.time()
    while True:
        try:
            response = requests.get(f"{API_LIST_SENSORS_URL}?key={api_key}", timeout=10)  # 10-second timeout for the request
            response.raise_for_status()
            return response.json()
        except requests.Timeout:
            if time.time() - start_time > 30:
                raise APILimitExceeded("Your BreatheLondon API Limit exceeded")
            time.sleep(1)  # Wait for 1 second before retrying
        except requests.RequestException as e:
            raise Exception(f"API request failed: {e}")

def process_sensor_data(json_data):
    flat_data = [item for sublist in json_data for item in sublist]
    return pd.DataFrame(flat_data)

def get_site_codes(df, limit=None):
    site_codes = df['SiteCode'].tolist()
    return site_codes[:limit] if limit else site_codes

def main(api_key=None, output_file=None, site_code_limit=5):
    try:
        api_key = get_api_key(api_key)
        json_data = fetch_sensor_data(api_key)
        df_sites_list = process_sensor_data(json_data)
        
        if not output_file:
            output_file = f"sensor_data_{pd.Timestamp.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"
        
        df_sites_list.to_csv(output_file, index=False)
        print(f"Full dataset saved to {output_file}")

        site_codes = get_site_codes(df_sites_list, limit=site_code_limit)
        print(f"Sample Site Codes (limit {site_code_limit}):", site_codes)

        return df_sites_list, site_codes, output_file

    except APILimitExceeded as e:
        print(str(e))
        return None, None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None, None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch and process Breathe London sensor data")
    parser.add_argument("--api_key", help="Your Breathe London API key")
    parser.add_argument("--output", help="Output CSV file name")
    parser.add_argument("--limit", type=int, default=5, help="Limit for sample site codes")
    args = parser.parse_args()

    df, codes, output_file = main(api_key=args.api_key, output_file=args.output, site_code_limit=args.limit)

#--------------------------------------------------------------#
# Usage in a python notebook:
# from breathe_london_api_list_sensors import main

# df, site_codes, output_file = main(api_key="YOUR_API_KEY", output_file="my_output.csv", site_code_limit=10)

# if df is None:
#     print("Failed to fetch data. Please check your API key and try again later.")
# else:
#     print(f"Data saved to: {output_file}")
#     print(f"First few site codes: {site_codes[:5]}")

#--------------------------------------------------------------#

# Usage in a terminal:
# python breathe_london_api.py --api_key YOUR_API_KEY --output my_output.csv --limit 10