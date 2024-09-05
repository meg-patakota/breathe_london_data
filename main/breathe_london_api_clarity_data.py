import requests
import os
import pandas as pd
from datetime import datetime, timedelta
import time
from dotenv import load_dotenv
import logging
import argparse

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
API_KEY = os.getenv('API_KEY')

# Constants
API_CLARITY_HOURLY_URL = "https://api.breathelondon.org/api/getClarityData/{siteCode}/{species}/{startTime}/{endTime}/{averaging}?key={apiKey}"

def get_clarity_data(siteCode, species, startTime, endTime, averaging):
    try:
        formatted_startTime = startTime.replace(" ", "%20")
        formatted_endTime = endTime.replace(" ", "%20")
        url = API_CLARITY_HOURLY_URL.format(siteCode=siteCode, species=species, startTime=formatted_startTime, endTime=formatted_endTime, averaging=averaging, apiKey=API_KEY)
        logger.info(f"Fetching data for {siteCode} and {species}")
        response = requests.get(url)
        if response.status_code == 200:
            sensors = response.json()
            sensors = pd.DataFrame.from_dict(sensors)
            logger.info(f"Successfully received data for {siteCode} and {species}")
            return sensors
        else:
            logger.error(f"Error with status code: {response.status_code}")
            logger.error(response.text)
            return None
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return None

def main(siteCodes, species, averaging, days, output_file=None):
    endTime = datetime.now()
    startTime = endTime - timedelta(days=days)
    endTime_str = endTime.strftime("%a %d %b %Y %H:%M:%S")
    startTime_str = startTime.strftime("%a %d %b %Y %H:%M:%S")

    df_list = []
    for siteCode in siteCodes:
        for specie in species:
            data = get_clarity_data(siteCode, specie, startTime_str, endTime_str, averaging)
            if data is not None and isinstance(data, pd.DataFrame):
                data['DateTime'] = pd.to_datetime(data['DateTime'])
                data['mod_datetime'] = data['DateTime'] + pd.Timedelta(hours=1)
                data['species'] = specie
                df_list.append(data)
            else:
                logger.warning(f"No data received for {siteCode} and {specie}")

    if df_list:
        df_all = pd.concat(df_list)
        logger.info(f"Total data shape: {df_all.shape}")
        logger.info(f"Latest data timestamp: {df_all.mod_datetime.max()}")
        logger.info(f"Number of unique sites: {df_all.SiteCode.nunique()}")
        
        if output_file is None:
            output_file = f"clarity_data_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"
        
        df_all.to_csv(output_file, index=False)
        logger.info(f"Data saved to {output_file}")
        return df_all
    else:
        logger.warning("No data received for all site codes and species.")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Breathe London Clarity Data")
    parser.add_argument("--sitecodes", nargs='+', default=["CLDP0001", "CLDP0002"], help="List of site codes")
    parser.add_argument("--species", nargs='+', default=["IPM25", "INO2"], help="List of species")
    parser.add_argument("--averaging", default="Hourly", help="Averaging period")
    parser.add_argument("--days", type=int, default=365, help="Number of days to fetch data for")
    parser.add_argument("--output", help="Output CSV file name")
    args = parser.parse_args()

    df = main(args.sitecodes, args.species, args.averaging, args.days, args.output)
    if df is not None:
        print(df.head())