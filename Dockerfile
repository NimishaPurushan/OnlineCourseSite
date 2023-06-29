FROM python:3.8.3

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN python3 manage.py makemigrations 
RUN python3 manage.py migrate
RUN python3 manage.py seed

# Expose port 8000 for the Django development server
EXPOSE 8000

# Start the Django development server

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]