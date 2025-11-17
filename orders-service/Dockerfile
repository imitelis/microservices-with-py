FROM python:3.12

WORKDIR /src

COPY . .
RUN pip install --no-cache-dir -r reqs.txt

CMD ["uvicorn", "src.main:create_app", "--host", "0.0.0.0", "--port", "8080"]
