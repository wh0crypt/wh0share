FROM python:3.11-slim

RUN useradd -m wh0user

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py utils.py ./
COPY templates ./templates
COPY static ./static

RUN mkdir -p /app/uploads && chown -R wh0user:wh0user /app/uploads

USER wh0user

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
