# Breathe London Data
[![Personal Project](https://img.shields.io/badge/Project-Personal-green)](https://meg-patakota.github.io)
[![by Meg Patakota](https://img.shields.io/badge/by-Meg%20Patakota-blue)](https://meg-patakota.github.io)

A Python tool to fetch and process air quality data from the Breathe London API.
Official Breathe London Developers documentation [here](https://www.breathelondon.org/developers).

## Features

- Fetch sensor data from the Breathe London API
- Save data to CSV format
- Flexible usage in both Python notebooks and command-line interface
- Configurable site code limit

## Installation

Clone this repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/breathe_london_data.git
cd breathe_london_data
pip install -r requirements.txt
```

## Usage

### In a Python Notebook

```python
# Usage to set the sitecodes required below
from breathe_london_api_list_sensors import main

df, site_codes, output_file = main(api_key="YOUR_API_KEY", output_file="my_output.csv", site_code_limit=10)

if df is None:
    print("Failed to fetch data. Please check your API key and try again later.")
else:
    print(f"Data saved to: {output_file}")
    print(f"First few site codes: {site_codes[:5]}")
```

```python
# Usage to get hourly data for the sitecodes of your choice
# Import the necessary functions and variables from your script
from breathe_london_api_clarity_data import main, get_clarity_data, API_KEY

# Test the get_clarity_data function
siteCode = "CLDP0001"
species = "IPM25"
endTime = datetime.now()
startTime = endTime - timedelta(days=7)
endTime_str = endTime.strftime("%a %d %b %Y %H:%M:%S")
startTime_str = startTime.strftime("%a %d %b %Y %H:%M:%S")
averaging = "Hourly"

data = get_clarity_data(siteCode, species, startTime_str, endTime_str, averaging)
if data is not None:
    print(data.head())
else:
    print("No data received")

# Test the main function
siteCodes = ["CLDP0001", "CLDP0002"]
species_list = ["IPM25", "INO2"]
days = 30

df = main(siteCodes, species_list, averaging, days)
if df is not None:
    print(df.head())
    print(f"Total data shape: {df.shape}")
    print(f"Latest data timestamp: {df.mod_datetime.max()}")
    print(f"Number of unique sites: {df.SiteCode.nunique()}")
else:
    print("No data received")
```

### From the Command Line

```bash
python breathe_london_api.py --api_key YOUR_API_KEY --output my_output.csv --limit 10
```

## Configuration

- `api_key`: Your Breathe London API key
- `output_file`: Name of the CSV file to save the data (default: "output.csv")
- `site_code_limit`: Maximum number of site codes to process (default: None, processes all available)

## Contributing

Contributions to this project are welcome! If you're interested in contributing or using this project, please follow these steps:

1. Check out my [GitHub.io page](https://meg-patakota.github.io) for contact details and more information about my work.
2. Feel free to open an issue to discuss potential changes or improvements.
3. If you'd like to make direct changes, please submit a Pull Request.

I appreciate your interest in my project and look forward to potential collaborations!

## License

This is a personal project created and maintained by Meg Patakota. All rights reserved. This project is not licensed for use, modification, or distribution without explicit permission from the author.

## Acknowledgments

- Breathe London for providing the air quality data API
<!-- - [Add any other acknowledgments here] -->