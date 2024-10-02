# Use the official Python image as a base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install required packages
RUN pip install -r requirements.txt

# Expose the port that Flask runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
