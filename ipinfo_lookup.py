import os
import requests
import streamlit as st
import pandas as pd

API_TOKEN = os.getenv("IPINFO_API_TOKEN")
CHECKED_IPS_FILE = os.getenv("CHECKED_IPS_FILE")
if not API_TOKEN:
    st.error("The IPINFO_API_TOKEN environment variable is not set.")
    st.stop()

def fetch_ipinfo_data(ip_address):
    url = f"https://ipinfo.io/{ip_address}/json?token={API_TOKEN}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def process_ips(ip_addresses):
    results = []
    for ip in ip_addresses:
        data = fetch_ipinfo_data(ip)
        results.append({
            "IP": ip,
            "Hostname": data.get("hostname", "N/A"),
            "City": data.get("city", "N/A"),
            "Region": data.get("region", "N/A"),
            "Country": data.get("country", "N/A"),
            "Org": data.get("org", "N/A"),
            "Latitude": data.get("loc", "N/A").split(",")[0] if "loc" in data else "N/A",
            "Longitude": data.get("loc", "N/A").split(",")[1] if "loc" in data else "N/A",
        })
    return results

def save_results_to_csv(results, output_file):
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)
    return output_file

def load_checked_ips():
    """Load previously checked IPs from the persistent file."""
    if os.path.exists(CHECKED_IPS_FILE):
        try:
            return pd.read_csv(CHECKED_IPS_FILE)["IP"].tolist()
        except Exception as e:
            return []
    return []

def save_checked_ips(checked_ips):
    """Save newly checked IPs to the persistent file."""
    if os.path.exists(CHECKED_IPS_FILE):
        existing_ips = pd.read_csv(CHECKED_IPS_FILE)
        new_ips_df = pd.DataFrame({"IP": list(checked_ips)})
        all_ips = pd.concat([existing_ips, new_ips_df]).drop_duplicates()
    else:
        all_ips = pd.DataFrame({"IP": list(checked_ips)})

    all_ips.to_csv(CHECKED_IPS_FILE, index=False)

def main():
    # Streamlit Interface
    st.title("IPInfo.io Geolocation Lookup")
    
    uploaded_file = st.file_uploader("Upload a CSV file containing IP addresses", type=["csv"])
    if uploaded_file:
        try:
            # Try to read the uploaded CSV file
            ip_df = pd.read_csv(uploaded_file)
            if ip_df.empty or ip_df.shape[1] < 1:
                st.error("The uploaded file is empty or does not contain a valid column.")
            else:
                # Assuming the first column contains IP addresses
                ip_df.columns = ["IP"]  # Rename the first column for clarity
                ip_df = ip_df.drop_duplicates()  # Remove duplicate IPs in the file

                checked_ips = set(load_checked_ips())
                new_ips = set(ip_df["IP"]) - checked_ips

                st.write(f"Found {len(new_ips)} new IP addresses to process (out of {len(ip_df)} total).")

                if len(new_ips) == 0:
                    st.info("No new IPs to process. All IPs in the file have already been checked.")
                elif st.button("Fetch Geolocation Data"):
                    with st.spinner("Fetching data, please wait..."):
                        results = process_ips(list(new_ips))
                        save_checked_ips(new_ips)

                    # Display results
                    results_df = pd.DataFrame(results)
                    st.success("Data fetching completed!")
                    st.dataframe(results_df)

                    # Downloadable CSV
                    output_csv = "results.csv"
                    save_results_to_csv(results, output_csv)
                    with open(output_csv, "rb") as file:
                        st.download_button(
                            label="Download Results as CSV",
                            data=file,
                            file_name="ipinfo_results.csv",
                            mime="text/csv"
                        )
        except pd.errors.EmptyDataError:
            st.error("The uploaded file is empty or not a valid CSV. Please upload a valid CSV file.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()