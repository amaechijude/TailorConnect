# Official python3.12
FROM python:3.12-slim

# Envorinment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONNUNBUFFERED=1

#work Directory
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# copy and install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install redis[ssl]

# Copy everything
COPY . .

