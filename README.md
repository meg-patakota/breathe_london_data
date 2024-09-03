# Breathe London Data
[![Personal Project](https://img.shields.io/badge/Project-Personal-blue)](https://meg-patakota.github.io)
[![by Meg Patakota](https://img.shields.io/badge/by-Meg%20Patakota-blue)](https://meg-patakota.github.io)

A Python tool to fetch and process air quality data from the Breathe London API.

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
from breathe_london_api_list_sensors import main

df, site_codes, output_file = main(api_key="YOUR_API_KEY", output_file="my_output.csv", site_code_limit=10)

if df is None:
    print("Failed to fetch data. Please check your API key and try again later.")
else:
    print(f"Data saved to: {output_file}")
    print(f"First few site codes: {site_codes[:5]}")
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

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This is a personal project created and maintained by Meg Patakota. All rights reserved. This project is not licensed for use, modification, or distribution without explicit permission from the author.
If you're interested in using or contributing to this project, please contact me directly at [your email or preferred contact method].

## Acknowledgments

- Breathe London for providing the air quality data API
- [Add any other acknowledgments here]