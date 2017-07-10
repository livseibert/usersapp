# Use an official Python runtime as a base image
FROM python:2.7-slim

# Set the working directory to /usersapp
WORKDIR /usersapp

# Copy the current directory contents into the container at /app
ADD . /usersapp

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "views.py"]