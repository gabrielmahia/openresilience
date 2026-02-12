FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY notifier ./notifier
CMD ["python","-m","notifier.main"]
