FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY config.json .
COPY setup_logger.py .
COPY main.py .
COPY create_session.py .
CMD ["python", "main.py"]