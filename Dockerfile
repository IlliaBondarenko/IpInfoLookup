# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script and input/output folders
COPY ipinfo_lookup.py .
COPY input_folder /app/input_folder
COPY output_folder /app/output_folder

# Set the default command to run the script
ENTRYPOINT ["python", "ipinfo_lookup.py"]
