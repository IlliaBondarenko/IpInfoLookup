import os
import requests
import streamlit as st
import pandas as pd

API_TOKEN = os.getenv("IPINFO_API_TOKEN")
CHECKED_IPS_FILE = os.getenv("CHECKED_IPS_FILE")
CHECKED_MAC_FILE = os.getenv("CHECKED_MAC_FILE")
if not API_TOKEN:
    st.error("The IPINFO_API_TOKEN environment variable is not set.")
    st.stop()
    
def get_ipinfo_api(ip_addres):
    ipinfo = format_ipinfo(fetch_ipinfo_data(ip_addres))
    csv_output = f"{ipinfo['IP']},{ipinfo['Hostname']},{ipinfo['City']},{ipinfo['Region']},{ipinfo['Country']},{ipinfo['Org']},{ipinfo['Latitude']},{ipinfo['Longitude']}"
    save_checked_ips([ip_addres])
    return csv_output

def get_macinfo_api(mac_address):
    restult = fetch_uoimac_data(mac_address)
    save_checked_macs([mac_address])
    return f"{restult['MAC']}"

def process_macs(mac_addresses):
    results = []
    for mac in mac_addresses:
        data = fetch_uoimac_data(mac)
        results.append(data)
    return results

def process_ips(ip_addresses):
    results = []
    for ip in ip_addresses:
        data = fetch_ipinfo_data(ip)
        formatted_data = format_ipinfo(data,False)
        results.append(formatted_data)
    return results

def format_ipinfo(data, full=True):
    result = {
        "Hostname": data.get("hostname", "N/A"),
        "City": data.get("city", "N/A"),
        "Region": data.get("region", "N/A"),
        "Country": data.get("country", "N/A"),
        "Org": data.get("org", "N/A"),
        "Latitude": data.get("loc", "N/A").split(",")[0] if "loc" in data else "N/A",
        "Longitude": data.get("loc", "N/A").split(",")[1] if "loc" in data else "N/A",
    }
    if full:
        result["IP"] = data.get("ip", "N/A")
    return result

def fetch_ipinfo_data(ip_address):
    url = f"https://ipinfo.io/{ip_address}/json?token={API_TOKEN}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def fetch_uoimac_data(mac_address):
    mac_prefix = str(mac_address).replace(":", "")[:6].upper()
    with open('MAC-by-Vendor.txt', 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.split("-")
            if len(parts) >= 3:
                oui = parts[1].replace(":", "").strip().upper()
                manufacturer = parts[2].strip()
                if oui == mac_prefix:
                    save_checked_macs([mac_address])
                    return {"MAC": manufacturer}
    return {"MAC": "N/A"}

def load_checked_ips():
    """Load previously checked IPs from the persistent file."""
    if os.path.exists(CHECKED_IPS_FILE):
        try:
            return pd.read_csv(CHECKED_IPS_FILE)["IP"].tolist()
        except Exception as e:
            return []
    return []

def load_checked_macs():
    """Load previously checked MACs from the persistent file."""
    if os.path.exists(CHECKED_MAC_FILE):
        try:
            return pd.read_csv(CHECKED_MAC_FILE)["MAC"].tolist()
        except Exception as e:
            return []
    return []

def save_checked_ips(checked_ips):
    if os.path.exists(CHECKED_IPS_FILE):
        existing_ips = pd.read_csv(CHECKED_IPS_FILE)
        new_ips_df = pd.DataFrame({"IP": list(checked_ips)})
        all_ips = pd.concat([existing_ips, new_ips_df]).drop_duplicates()
    else:
        all_ips = pd.DataFrame({"IP": list(checked_ips)})

    all_ips.to_csv(CHECKED_IPS_FILE, index=False)

def save_checked_macs(checked_macs):
    if os.path.exists(CHECKED_MAC_FILE):
        existing_macs = pd.read_csv(CHECKED_MAC_FILE)
        new_mac = pd.DataFrame({"MAC": checked_macs})
        all_macs = pd.concat([existing_macs, new_mac]).drop_duplicates()
    else:
        all_macs = pd.DataFrame({"MAC": checked_macs})

    all_macs.to_csv(CHECKED_MAC_FILE, index=False)
     
def main():
    st.title("IPInfo.io Geolocation Lookup")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        try:
            # Read the uploaded CSV file
            csv_df = pd.read_csv(uploaded_file)
            # Ensure all column names are strings to avoid warnings
            csv_df.columns = csv_df.columns.map(str)
            # Allow the user to select processing options
            process_ip_column = st.checkbox("Do you want to process an IP address column?", value=True)
            process_mac_column = st.checkbox("Do you want to process a MAC address column?")

            # Ensure at least one column is selected
            if not process_ip_column and not process_mac_column:
                st.error("Please select at least one column to process.")
            else:
                column_options = csv_df.columns.tolist()
            # Initialize lists for IPs and MACs
            ips_to_process = []
            macs_to_process = []

            # IP column selection
            if process_ip_column:
                selected_ip_column = st.selectbox("Select the column containing IP addresses:", column_options)
                ip_df = csv_df[[selected_ip_column]].rename(columns={selected_ip_column: "IP"})
                ips_to_process = ip_df["IP"].tolist()  # Process all IPs
                st.write(f"Found {len(ips_to_process)} IP addresses to process.")

            # MAC column selection
            if process_mac_column:
                selected_mac_column = st.selectbox("Select the column containing MAC addresses:", column_options)
                mac_df = csv_df[[selected_mac_column]].rename(columns={selected_mac_column: "MAC"})
                macs_to_process = mac_df["MAC"].tolist()  # Process all MACs
                st.write(f"Found {len(macs_to_process)} MAC addresses to process.")

            # Processing logic
            if len(ips_to_process) == 0 and len(macs_to_process) == 0:
                st.info("No IPs or MACs selected for processing.")
            elif st.button("Fetch Geolocation Data"):
                with st.spinner("Fetching data, please wait..."):
                    results = []

                    # Process IPs
                    if process_ip_column and len(ips_to_process) > 0:
                        ip_results = process_ips(ips_to_process)
                        save_checked_ips(ips_to_process)  # Save processed IPs
                        ip_results_df = pd.DataFrame(ip_results)
                        results.append(ip_results_df)

                    # Process MACs
                    if process_mac_column and len(macs_to_process) > 0:
                        mac_results = process_macs(macs_to_process)
                        save_checked_macs(macs_to_process)  # Save processed MACs
                        mac_results_df = pd.DataFrame(mac_results)
                        results.append(mac_results_df)

                    # Combine all results
                    if results:
                        # Reset indices for the original DataFrame and result DataFrame
                        csv_df = csv_df.reset_index(drop=True)
                        combined_results_df = pd.concat(results, axis=1) if len(results) > 1 else results[0]
                        combined_results_df = combined_results_df.reset_index(drop=True)

                        # Concatenate original CSV with results
                        combined_df = pd.concat([csv_df, combined_results_df], axis=1)
                        st.success("Data fetching completed!")
                        st.dataframe(combined_df)
                    else:
                        st.error("No data was processed.")
                            
        except pd.errors.EmptyDataError:
            st.error("The uploaded file is empty or not a valid CSV. Please upload a valid CSV file.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()