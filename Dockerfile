FROM python:3.12-slim

WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# COPY build.sh .
RUN bash build.sh

EXPOSE 8080

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
