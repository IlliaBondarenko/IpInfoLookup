### **`README.md`**

# IPInfo Geolocation Lookup

This project uses the IPInfo API to perform geolocation lookups for IP addresses. It reads CSV files containing IP addresses from a folder, queries the IPInfo API for each IP, and saves the results in JSON and CSV formats.

## Getting Started

### Prerequisites

1. **Docker**: This project is containerized with Docker. Make sure you have Docker installed on your system.
   - [Docker Installation Guide](https://docs.docker.com/get-docker/)

2. **Docker Compose**: You'll need Docker Compose to easily manage the multi-container application.
   - [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)

3. **IPInfo API Token**: You’ll need a valid IPInfo API token to use the geolocation service.

---

### Step 1: Get Your IPInfo API Token

1. Go to [IPInfo.io](https://ipinfo.io/signup) and sign up for an account.
2. After signing in, go to your [IPInfo dashboard](https://ipinfo.io/account).
3. Copy your **API Token** from the dashboard.

---

### Step 2: Add Your API Token to `.env`

1. In the project directory, create a `.env` file if it doesn't already exist.
2. Add your IPInfo API token to the `.env` file as follows:
   ```
   IPINFO_API_TOKEN=your_api_token_here
   ```
   Replace `your_api_token_here` with the token you copied from the IPInfo dashboard.

---

### Step 3: Running the Docker Container

1. **Add the files to scan**:
    Copy all the cvs files you need to scan into the input_folder

2. **Build the Docker Image and Run the Docker Container**:
   Open your terminal and navigate to the project directory. Then, run:
   ```bash
   docker-compose up --build
   ```
   This will build the Docker image, installing all necessary dependencies and start the container, which will:
   - Scan all `.csv` files in the `input_folder/`
   - Perform IP lookups using the IPInfo API
   - Save the results in the `output_folder/` as JSON files

3. **Stop the Container**:
   You can stop the container by pressing `Ctrl + C` in the terminal or running:
   ```bash
   docker-compose down
   ```

---

### Folder Structure

```
ipinfo-docker/
├── ipinfo_lookup.py        # Python script for IP lookup
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Docker Compose configuration
├── .env                    # Contains your IPInfo API token
├── input_folder/           # Folder with input CSV files (IP addresses)
├── output_folder/          # Folder for saving output JSON results
└── .gitignore              # Files to ignore in Git
```

### Folder Details

- **input_folder/**: Place your CSV files containing IP addresses here. Each CSV file should have IPs in the first column.
- **output_folder/**: This is where the JSON results will be saved. Each input CSV file will have a corresponding JSON file saved here.
- **.gitignore**: Ensures sensitive files like `.env` and output data are not tracked by Git.

---

### Example CSV Format

CSV files should have IP addresses in the first column. An example `ips.csv` might look like this:

```
IP Address
8.8.8.8
8.8.4.4
```

---

### Troubleshooting

- Ensure that your `.env` file is correctly populated with a valid IPInfo API token.
- If Docker fails to build, try running `docker-compose build --no-cache` to force a clean rebuild.
- If you're encountering rate limits, you might need to upgrade your IPInfo plan.

---

This `README.md` provides a comprehensive guide to getting started with the IPInfo geolocation lookup project using Docker.