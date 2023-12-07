# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Print the current working directory
RUN pwd

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# # Make port 8000 available to the world outside this container
# EXPOSE 8000

# # Define environment variable
# ENV NAME World

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003"]
