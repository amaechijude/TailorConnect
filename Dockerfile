FROM python:3.10

# WORKDIR /app

# COPY requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# # Use an official Python runtime as a parent image
# FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt
RUN bash build.sh


# Copy the rest of the project files into the container
COPY . /app/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Collect static files (you might need this for production)
# RUN python manage.py collectstatic --noinput

# Run migrations
# RUN python manage.py migrate

# Expose the port the app runs on
EXPOSE 8000

# Command to run the Django app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "TailorConnect.wsgi:application"]
