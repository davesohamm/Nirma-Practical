FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install flask pymongo

EXPOSE 8001

CMD ["python", "db_app.py"]