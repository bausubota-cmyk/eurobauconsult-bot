FROM python:3.10-slim

WORKDIR /app

# Сначала зависимости — кэш слоя не будет инвалидироваться при правках кода
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Потом код
COPY . .

# Меньше буферизации в логах + не писать .pyc
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

CMD ["python", "eurobau.py"]
