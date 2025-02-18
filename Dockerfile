# Use Python 3.10 as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY . /app

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install the required dependencies
RUN pip install -r requirements.txt

# Expose port 5000 to allow external access
EXPOSE 5000

# Run the Flask application using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

#run below code on terminal to run Docker:
# docker build -t diabetes_app .
# docker run -p 5000:5000 diabetes_app