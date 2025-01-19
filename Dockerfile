# Use a lightweight Python image as the base image
FROM python:3.9-slim

# Set environment variables inside the Dockerfile
# ENV IPINFO_API_TOKEN=cab2989aec4413

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the default Streamlit port
EXPOSE 8501

# Set Streamlit configuration to allow access from all network interfaces
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Command to run the Streamlit app
CMD ["streamlit", "run", "ipinfo_lookup.py"]
