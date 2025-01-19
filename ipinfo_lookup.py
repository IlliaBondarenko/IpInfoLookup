import os
import csv
import requests
import argparse
import time
import sys

# Get the API token from the environment variable
API_TOKEN = os.getenv("IPINFO_API_TOKEN")
if not API_TOKEN:
    raise ValueError("The IPINFO_API_TOKEN environment variable is not set.")

def fetch_ipinfo_data(ip_address):
    url = f"https://ipinfo.io/{ip_address}/json?token={API_TOKEN}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {ip_address}: {e}")
        return {"error": str(e)}

def read_ips_from_csv(csv_file):
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

def save_results_to_csv(data, output_file):
    try:
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            # Write header row
            writer.writerow(['IP', 'Hostname', 'City', 'Region', 'Country', 'Org', 'Latitude', 'Longitude'])
            
            for ip, info in data.items():
                hostname = info.get('hostname', 'N/A')
                city = info.get('city', 'N/A')
                region = info.get('region', 'N/A')
                country = info.get('country', 'N/A')
                org = info.get('org', 'N/A')
                loc = info.get('loc', 'N/A').split(',')
                
                # Extract latitude and longitude
                latitude = loc[0] if len(loc) > 0 else 'N/A'
                longitude = loc[1] if len(loc) > 1 else 'N/A'
                
                writer.writerow([ip, hostname, city, region, country, org, latitude, longitude])
        print(f"Location data saved to {output_file}")
    except IOError as e:
        print(f"Error saving results to {output_file}: {e}")

def save_checked_ips(checked_ips, checked_ips_file):
    try:
        with open(checked_ips_file, 'a', newline='') as file:
            writer = csv.writer(file)
            for ip in checked_ips:
                writer.writerow([ip])
        print(f"Checked IPs saved to {checked_ips_file}")
    except IOError as e:
        print(f"Error saving checked IPs to {checked_ips_file}: {e}")

def process_folder(input_folder, output_folder, checked_ips_file):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Read previously checked IPs
    checked_ips = set(read_ips_from_csv(checked_ips_file))
    all_results = {}
    new_checked_ips = set()

    for filename in os.listdir(input_folder):
        if filename.endswith(".csv"):
            input_file = os.path.join(input_folder, filename)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_csv_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_{timestamp}.csv")
            
            print(f"Processing file: {input_file}")
            ip_addresses = read_ips_from_csv(input_file)

            results = {}
            for ip in ip_addresses:
                if ip not in checked_ips:
                    print(f"Fetching data for IP: {ip}")
                    data = fetch_ipinfo_data(ip)
                    results[ip] = data
                    new_checked_ips.add(ip)

            if results:
                save_results_to_csv(results, output_csv_file)

    # Check if any new IPs were processed
    if new_checked_ips:
        # Save the new checked IPs to the checked_ips file
        save_checked_ips(new_checked_ips, checked_ips_file)
        return 0  # Successful run with new IPs processed
    else:
        print("No new IPs found. Exiting script.")
        return 1  # Exit with non-zero code to stop Docker

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="IPInfo.io Geolocation Lookup Script")
    parser.add_argument("input_folder", help="Path to the folder containing CSV files with IP addresses")
    parser.add_argument("output_folder", help="Path to the folder to save CSV results")
    parser.add_argument("checked_ips_file", help="Path to the CSV file tracking previously checked IPs")
    args = parser.parse_args()

    # Process the folder
    exit_code = process_folder(args.input_folder, args.output_folder, args.checked_ips_file)

    # Exit the script with the appropriate exit code
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
