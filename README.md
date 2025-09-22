# microservices-with-py

Microservices backend example using FastAPI and Kafka

## first-service (single server kafka topic)

  *  `cd first-service`
  *  `python3 -m venv venv`
  *  `source venv/bin/activate`
  *  `pip install -r reqs.txt`
  *  same folder other terminal `docker-compose up`
  *  `uvicorn app.main:app --reload`

## micro-services (several servers kafka topics)
  *  first-service-kafka-1
  *  first-service-zookeeper-1  

### Microservices architecture
graph TD
    subgraph Customer Service
        A1[Customer API]
        A2[(PostgreSQL)]
    end

    subgraph Orders Service
        B1[Orders API]
        B2[(PostgreSQL)]
    end

    subgraph Inventory Service
        C1[Inventory API]
        C2[(MongoDB)]
    end

    subgraph Billing Service
        D1[Billing API]
        D2[(PostgreSQL)]
    end

    subgraph Notification Service
        E1[Notifications API]
        E2[(Redis)]
    end

    A1 -->|HTTP| B1
    A1 --> A2
    B1 --> B2
    B1 -->|HTTP| C1
    B1 -->|HTTP| D1
    C1 --> C2
    D1 --> D2
    C1 -->|HTTP| E1
    D1 -->|HTTP| E1
    E1 --> E2

### Event flow via Kafka topics
graph TD
    subgraph Kafka Topics
        T1((customer.created))
        T2((order.created))
        T3((order.paid))
        T4((stock.updated))
        T5((low.stock))
    end

    A[Customer Service] --> T1
    T1 --> B[Orders Service]
    B --> T2
    T2 --> C[Inventory Service]
    T2 --> D[Billing Service]
    C --> T4
    C --> T5
    T4 --> E[Notification Service]
    T5 --> E
    D --> T3
    T3 --> E

### Service responsability map
classDiagram
    class CustomerService {
        +POST /customers
        +GET /customers/{id}
        DB: SQLite
        Publishes: customer.created
    }

    class OrdersService {
        +POST /orders
        +GET /orders/{id}
        DB: SQLite
        Consumes: customer.created
        Publishes: order.created
    }

    class InventoryService {
        +GET /stock/{sku}
        +POST /stock/reserve
        DB: SQLite
        Consumes: order.created
        Publishes: stock.updated, low.stock
    }

    class BillingService {
        +POST /billing
        DB: SQLite
        Consumes: order.created
        Publishes: order.paid
    }

    class NotificationService {
        +POST /notify
        DB: Redis
        Consumes: stock.updated, low.stock, order.paid
    }
