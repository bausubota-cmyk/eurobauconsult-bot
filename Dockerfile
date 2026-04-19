FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir aiogram==2.25.1 openai python-dotenv
COPY . .
CMD ["python", "eurobau.py"]
