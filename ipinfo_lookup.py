import os
import csv
import requests
import json
import argparse

# Get the API token from the environment variable
API_TOKEN = os.getenv("IPINFO_API_TOKEN")
if not API_TOKEN:
    raise ValueError("The IPINFO_API_TOKEN environment variable is not set.")

def fetch_ipinfo_data(ip_address):
    """
    Fetch geolocation data from ipinfo.io for a given IP address.
    """
    url = f"https://ipinfo.io/{ip_address}/json?token={API_TOKEN}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {ip_address}: {e}")
        return {"error": str(e)}

def read_ips_from_csv(csv_file):
    """
    Read a list of IP addresses from a CSV file.
    Assumes the IPs are in the first column.
    """
    ip_list = []
    try:
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            # Skip the header row if it exists
            next(reader, None)
            for row in reader:
                if row:  # Ensure the row is not empty
                    ip_list.append(row[0].strip())
    except FileNotFoundError:
        print(f"File {csv_file} not found.")
    return ip_list

def save_results_to_json(data, output_file):
    """
    Save the fetched results to a JSON file.
    """
    try:
        with open(output_file, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Results saved to {output_file}")
    except IOError as e:
        print(f"Error saving results to {output_file}: {e}")

def save_results_to_csv(data, output_file):
    """
    Save the fetched IP and location data to a CSV file.
    """
    try:
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['IP', 'Location'])
            for ip, info in data.items():
                loc = info.get('loc', 'N/A')  # Use 'N/A' if no location is available
                writer.writerow([ip, loc])
        print(f"Location data saved to {output_file}")
    except IOError as e:
        print(f"Error saving results to {output_file}: {e}")

def process_folder(input_folder, output_folder):
    """
    Process all CSV files in a folder, performing IP lookups for each file.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".csv"):
            input_file = os.path.join(input_folder, filename)
            output_json_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_results.json")
            output_csv_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_locations.csv")
            
            print(f"Processing file: {input_file}")
            ip_addresses = read_ips_from_csv(input_file)

            results = {}
            for ip in ip_addresses:
                print(f"Fetching data for IP: {ip}")
                results[ip] = fetch_ipinfo_data(ip)
            
            save_results_to_json(results, output_json_file)
            save_results_to_csv(results, output_csv_file)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="IPInfo.io Geolocation Lookup Script")
    parser.add_argument("input_folder", help="Path to the folder containing CSV files with IP addresses")
    parser.add_argument("output_folder", help="Path to the folder to save JSON results")
    args = parser.parse_args()

    # Process the folder
    process_folder(args.input_folder, args.output_folder)

if __name__ == "__main__":
    main()
