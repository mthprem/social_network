# Use the official Python image as a base
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /social_network

# Copy the requirements file into the container
COPY requirements.txt /social_network/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
#RUN python manage.py makemigrations
#RUN python manage.py migrate

# Copy the Django project files into the container
COPY . /social_network/

# Apply database migrations
RUN python manage.py migrate
