# Use a lightweight Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose both ports
EXPOSE 8000 8501

# Set environment variables inside the Dockerfile
ENV IPINFO_API_TOKEN=cab2989aec4413

# Run the combined script
CMD ["python", "app.py"]