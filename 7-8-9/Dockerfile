FROM python:3.9-slim
RUN apt-get update && apt-get install -y libpq-dev gcc graphviz && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Esta línea es la que copia las carpetas templates y static:
COPY . . 
CMD ["python", "app.py"]