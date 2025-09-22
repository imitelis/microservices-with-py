FROM python:3.12

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r reqs.txt

CMD ["uvicorn", "app.main:create_app", "--host", "0.0.0.0", "--port", "8080"]
