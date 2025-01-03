# TailorConnect

**TailorConnect** is an online platform designed to facilitate seamless connections between fashion designers and customers. Built with Django, the platform integrates multiple services like Azure for cloud storage, Redis for caching, and Celery for task management, all deployed in a Dockerized environment.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Deployment](#deployment)

## Features

- **User Authentication**: Secure sign-up and login functionality for customers and fashion designers and password reset via email.
- **Designer Profiles**: Fashion designers can showcase their work and list their services.
- **Customer Requests**: Customers can post requests for specific fashion needs and connect with designers.
- **Media Management**: Azure Blob Storage integration for storing static and media files.
- **Asynchronous Tasks**: Celery with Redis handles background tasks like sending emails and notifications.
- **Scalable Architecture**: Dockerized environment for consistent development and production setups.
- **Payment Integration**: Self-developed Python library [python-ercas-ng](https://pypi.org/project/python-ercas-ng/1.0.0/) a python wrapper of [ErcasNg](https://docs.ercaspay.com/) payment Api for handling secure payment transactions.

## Tech Stack

- **Backend**: Python, Django
- **Database**: PostgreSQL (Azure Flexible Server)
- **Frontend**: Django Templates with Bootstrap CSS and JavaScript
- **Caching**: Redis (Redis Docker image)
- **Task Queue**: Celery
- **Cloud Storage**: Azure Blob Storage
- **Payment**: [python-ercas-ng](https://pypi.org/project/python-ercas-ng/1.0.0/)
- **Deployment**: Docker, Azure Virtual Machine, etc.

## Installation

### Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Azure Account (for database, storage) or any alternative
- Redis
### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/amaechijude/tailorconnect.git
   cd tailorconnect
   ```

2. Set up a virtual environment and install dependencies:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file and configure it with the following variables:
```env
   DEBUG=True
   SECRET_KEY=your_secret_key
   DATABASE_URL=postgresql://username:password@host:port/dbname
   REDIS_URL=redis://username:password@host:port/0
   AZURE_STORAGE_ACCOUNT_NAME=your_account_name
   AZURE_STORAGE_ACCOUNT_KEY=your_account_key
   ```

4. Run database migrations:
```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create Superuser
```bash
python manage.py createsuperuser
```

## Configuration

- **Docker**: The `docker-compose.yml` file defines services for Django, Redis and Celery.
- **Azure Blob Storage**: Configure static and media file storage in `settings.py`.
- **Celery**: Set up workers for task queue management.
- **Payment Integration**: Configure [python-ercas-ng](https://pypi.org/project/python-ercas-ng/1.0.0/) for handling payment transactions.

## Usage

- **Run Dockerized Services**:
```bash
docker-compose -f docker-compose.dev.yaml up
```

- **Access the Application**:
  Navigate to `http://localhost:8000` in your browser.

- **Admin Panel**:
  Access the Django admin interface at `/admin`.

## Deployment

1. Deploy to Azure Virtual Machine using Docker Compose.
```bash
   ssh user@your-vm-ip
   git clone https://github.com/amaechijude/tailorconnect.git
   cd tailorconnect
   docker-compose -f docker-compose.prod.yaml up -d
   ```

2. Configure DNS and SSL (e.g., with Azure DNS and Let's Encrypt).
