# IPInfo Geolocation Lookup FastAPI & Streamlit Integration

This project provides a user-friendly interface to perform IP geolocation lookups using the [IPInfo API](https://ipinfo.io). The app, built with Streamlit, allows users to upload a CSV file containing IP addresses, filters out duplicates and previously checked IPs, and fetches geolocation data. Results can be downloaded as a CSV file. Additionally, a FastAPI backend is integrated to allow IP and MAC address lookups through API endpoints.

---

## Features

- **FastAPI**:
  - Provides two POST endpoints for IP and MAC address lookups.
  - `/ip/{ip}`: Fetches geolocation data for a given IP address.
  - `/oui/{mac_address}`: Fetches manufacturer information for a given MAC address.

- **Streamlit**:
  - Allows users to upload a CSV file containing IP addresses.
  - Filters out duplicates and previously checked IPs stored in `checked_ips.csv`.
  - Fetches geolocation data for new IPs and displays the results in an easy-to-use interface.
  - Allows users to download the results as a CSV file.

- Both **FastAPI** and **Streamlit** run concurrently in separate threads.

---

## Getting Started

### Prerequisites

1. **Docker**: This project is containerized with Docker. Install Docker on your system.
   - [Docker Installation Guide](https://docs.docker.com/get-docker/)

2. **Docker Compose**: You'll need Docker Compose to manage the container.
   - [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)

3. **IPInfo API Token**: Obtain a valid API token to access IPInfo's geolocation service.

---

### Step 1: Get Your IPInfo API Token

1. Sign up at [IPInfo.io](https://ipinfo.io/signup) for an account.
2. Access your [IPInfo dashboard](https://ipinfo.io/account).
3. Copy your **API Token** from the dashboard.

---

### Step 2: Add Your API Token to `docker-compose.yml`

1. Open `docker-compose.yml` and locate:
   ```yaml
   IPINFO_API_TOKEN: your_api_token_here
   ```
2. Replace `your_api_token_here` with the token you copied from the IPInfo dashboard.

---

### Step 3: Running the Application

1. **Build and Run the Docker Container**:
   Open your terminal, navigate to the project directory, and run:
   ```bash
   docker-compose up --build
   ```
   This will:
   - Build the Docker image and install all required dependencies.
   - Launch the Streamlit app at `http://localhost:8501`.

2. **Access the Application**:
   Open your browser and navigate to `http://localhost:8501`.

3. **Upload a CSV File**:
   - Upload a file containing IP addresses (one per row).
   - The app removes duplicates and skips IPs already stored in `checked_ips.csv`.
   - It fetches geolocation data for new IPs and allows you to download the results.

4. **Access the FastAPI Endpoints**:
   - The FastAPI app runs on `http://localhost:8000`.
   - You can access the following endpoints:
     - **POST /ip/{ip}**: Fetches IP information.
     - **POST /oui/{mac_address}**: Fetches manufacturer information from the MAC address.

---

### File Details

- **`checked_ips.csv`**: Tracks previously processed IPs, preventing duplicate API calls across sessions.
- **`checked_mac.csv`**: Tracks previously processed Mac addresses.
- **`docker-compose.yml`**: Configures and runs the Docker container, including API token setup.
- **`ipinfo_lookup.py`**: Main script that runs the Streamlit app.
- **`app.py`**: Contains the FastAPI app that runs alongside Streamlit to provide additional IP and MAC address lookup functionality.

---

### Example CSV Input Format

Upload a CSV file with IPs in the first column. Example:

```
IP
8.8.8.8
8.8.4.4
```

---
