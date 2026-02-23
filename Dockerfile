FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure the analytics directory exists if it doesn't
RUN mkdir -p kb/analytics

EXPOSE 8000

CMD ["python", "app.py"]
