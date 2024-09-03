# Breathe London Data

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Breathe London for providing the air quality data API
- [Add any other acknowledgments here]