# breathe_london_data

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