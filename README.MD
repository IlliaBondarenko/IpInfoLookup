# IPInfo Geolocation Lookup (Streamlit)

This project provides a user-friendly interface to perform IP geolocation lookups using the [IPInfo API](https://ipinfo.io). The app, built with Streamlit, allows users to upload a CSV file containing IP addresses, filters out duplicates and previously checked IPs, and fetches geolocation data. Results can be downloaded as a CSV file.

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

---

### Folder Structure

```
ipinfo-streamlit/
├── .gitignore              # Files to ignore in Git
├── checked_ips.csv         # Persistent file storing previously checked IPs
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker image configuration
├── ipinfo_lookup.py        # Streamlit-based IP lookup script
└── requirements.txt        # Python dependencies
```

### File Details

- **`checked_ips.csv`**: Tracks previously processed IPs, preventing duplicate API calls across sessions.
- **`docker-compose.yml`**: Configures and runs the Docker container, including API token setup.
- **`ipinfo_lookup.py`**: Main script that runs the Streamlit app.

---

### Example CSV Input Format

Upload a CSV file with IPs in the first column. Example:

```
IP
8.8.8.8
8.8.4.4
```

---

### Troubleshooting

- **Missing API Token**: Ensure `docker-compose.yml` has a valid IPInfo API token.
- **Empty File Error**: Make sure the uploaded CSV file is not empty and formatted correctly.
- **Rate Limits**: If you exceed IPInfo's rate limits, consider upgrading your IPInfo plan.

---

This `README.md` outlines how to run the IPInfo lookup application with Streamlit and Docker, ensuring an efficient, user-friendly experience for IP geolocation lookups.