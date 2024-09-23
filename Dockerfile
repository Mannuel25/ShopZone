FROM python:3.10.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    libpq-dev build-essential

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Command to run Django's development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
