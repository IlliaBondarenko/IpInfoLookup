#!/usr/bin/env python3
import os
import re
import csv

# Regular expression pattern to match a period-separated MAC address.
# This matches three groups of exactly four hexadecimal digits separated by periods.
mac_pattern = re.compile(r'\b(?:[0-9A-Fa-f]{4}\.){2}[0-9A-Fa-f]{4}\b')

def extract_mac_addresses(filepath):
    with open(filepath, 'r') as file:
        text = file.read()
    mac_addresses = mac_pattern.findall(text)
    # Remove duplicates while preserving order
    unique_mac_addresses = list(dict.fromkeys(mac_addresses))
    return unique_mac_addresses

def save_to_csv(mac_addresses, output_filepath):
    with open(output_filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["address"])
        for mac in mac_addresses:
            writer.writerow([mac])
    print(f"Saved {len(mac_addresses)} MAC address(es) to '{output_filepath}'")

def process_txt_files(directory):
    for filename in os.listdir(directory):
        if filename.lower().endswith('.txt'):
            txt_filepath = os.path.join(directory, filename)
            print(f"\nProcessing file: {txt_filepath}")
            mac_addresses = extract_mac_addresses(txt_filepath)
            if mac_addresses:
                # Create output CSV file with the same basename as the txt file.
                base_name = os.path.splitext(filename)[0]
                csv_filepath = os.path.join(directory, base_name + '.csv')
                save_to_csv(mac_addresses, csv_filepath)
            else:
                print("No MAC addresses found in the file.")

def process_txts():
    data_directory = 'data'  # Change this path if necessary.
    if not os.path.isdir(data_directory):
        print(f"Error: Directory '{data_directory}' does not exist.")
        return
    process_txt_files(data_directory)
