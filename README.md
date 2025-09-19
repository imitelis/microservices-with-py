# microservices-with-py

Microservices backend example using FastAPI and Kafka

## first-service (single server kafka topic)

  *  `cd first-service`
  *  `python3 -m venv venv`
  *  `source venv/bin/activate`
  *  `pip install -r ./reqs.txt`
  *  `docker-compose up`
  *  `uvicorn app.main:app --reload`

## micro-services (several servers kafka topics)

