# Use a lightweight Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables (you can also add these in your docker-compose.yml)
ENV IPINFO_API_TOKEN=your_api_token_here

# Make sure the script has execute permissions (if needed)
RUN chmod +x ipinfo_lookup.py

# Command to run the script (adjust for your needs)
CMD ["python", "ipinfo_lookup.py", "/input_folder", "/output_folder", "checked_ips.csv"]
