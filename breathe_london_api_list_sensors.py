import os
import requests
import pandas as pd
import argparse
from dotenv import load_dotenv
import time
import logging

class APILimitExceeded(Exception):
    pass

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)

logger = setup_logging()

def get_api_key(provided_key=None):
    if provided_key:
        logger.info("Using provided API key")
        return provided_key
    
    logger.info("Attempting to load API key from environment variables")
    load_dotenv()
    api_key = os.getenv('API_KEY')
    
    if not api_key:
        logger.error("API_KEY not found in environment variables")
        raise ValueError("API_KEY not found. Please provide it as an argument or set it in your environment variables.")
    
    logger.info("API key loaded successfully from environment variables")
    return api_key

def fetch_sensor_data(api_key):
    API_LIST_SENSORS_URL = "https://api.breathelondon.org/api/ListSensors"
    
    logger.info("Initiating API request to fetch sensor data")
    start_time = time.time()
    attempt = 1
    while True:
        try:
            logger.info(f"Attempt {attempt} to fetch data")
            response = requests.get(f"{API_LIST_SENSORS_URL}?key={api_key}", timeout=10)
            response.raise_for_status()
            logger.info("Data fetched successfully")
            return response.json()
        except requests.Timeout:
            elapsed_time = time.time() - start_time
            if elapsed_time > 30:
                logger.error("API request timed out after 30 seconds")
                raise APILimitExceeded("Your BreatheLondon API Limit exceeded")
            logger.warning(f"Request timed out. Retrying... (Elapsed time: {elapsed_time:.2f}s)")
            time.sleep(1)
            attempt += 1
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise Exception(f"API request failed: {e}")

def process_sensor_data(json_data):
    logger.info("Processing fetched sensor data")
    flat_data = [item for sublist in json_data for item in sublist]
    df = pd.DataFrame(flat_data)
    logger.info(f"Processed data into DataFrame with {len(df)} rows and {len(df.columns)} columns")
    return df

def get_site_codes(df, limit=None):
    logger.info("Extracting site codes from DataFrame")
    site_codes = df['SiteCode'].tolist()
    if limit:
        logger.info(f"Limiting site codes to {limit}")
        return site_codes[:limit]
    return site_codes

def main(api_key=None, output_file=None, site_code_limit=5):
    try:
        logger.info("Starting main process")
        api_key = get_api_key(api_key)
        json_data = fetch_sensor_data(api_key)
        df_sites_list = process_sensor_data(json_data)
        
        if not output_file:
            output_file = f"sensor_data_{pd.Timestamp.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"
        
        logger.info(f"Saving data to {output_file}")
        df_sites_list.to_csv(output_file, index=False)
        logger.info(f"Full dataset saved to {output_file}")

        site_codes = get_site_codes(df_sites_list, limit=site_code_limit)
        logger.info(f"Sample Site Codes (limit {site_code_limit}): {site_codes}")

        return df_sites_list, site_codes, output_file

    except APILimitExceeded as e:
        logger.error(str(e))
        return None, None, None
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None, None, None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch and process Breathe London sensor data")
    parser.add_argument("--api_key", help="Your Breathe London API key")
    parser.add_argument("--output", help="Output CSV file name")
    parser.add_argument("--limit", type=int, default=5, help="Limit for sample site codes")
    args = parser.parse_args()

    logger.info("Script started")
    df, codes, output_file = main(api_key=args.api_key, output_file=args.output, site_code_limit=args.limit)
    if df is not None:
        logger.info("Script completed successfully")
    else:
        logger.warning("Script completed with errors")

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