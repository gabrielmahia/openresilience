FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY worker ./worker
COPY shared/or_shared ./or_shared
ENV PYTHONPATH=/app
CMD ["python","-m","worker.main"]
