FROM python:3.11-slim

WORKDIR /app

# Install netcat (required for wait-for-db.sh)
RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

COPY . /app/

CMD ["/wait-for-db.sh", "python", "manage.py", "runserver", "0.0.0.0:8000"]
