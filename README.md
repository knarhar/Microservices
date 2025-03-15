# Microservices


## Project description

### Goal:

Create a simple microservice application that simulates the operation of an online store. Users can register view products and make purchases. Each service is responsible for its own part of the functionality.


### Logic:

1. User registers using **Auth Service**.
2. User explores products using **Product Service**.
3. User makes purchase:
   - Product Service sends order to **RabbitMQ**.
   - Payment Service processes the order and updates the payment status.


## Structure

```
microservices/
├── auth/                     # Auth Service (FastAPI)
│   ├── app/                  # Main code
│   │   ├── main.py           # Entry point
│   │   ├── models.py         # Data models (PostgreSQL)
│   │   ├── schemas.py        # Pydantic schemas
│   │   └── utils.py          # Utillities (ex. JWT)
│   ├── requirements.txt      # Dependencies
│   └── venv/                 # Virtual enviroment
│
├── product/                  # Product Service (Django)
│   ├── manage.py             # Django CLI
│   ├── product/              # Main app
│   │   ├── models.py         # Data models (PostgreSQL)
│   │   ├── views.py          # API endpoints
│   │   └── urls.py           # Routes
│   ├── requirements.txt      # Dependencies
│   └── venv/                 # Virtual Enviroment
│
├── payment/                  # Payment Service (Flask)
│   ├── app.py                # Entry point
│   ├── requirements.txt      # Dependencies
│   └── venv/                 # Virtual Enviroment
│
├── rabbitmq/                 # RabbitMQ (Windows installation)
└── README.md                 # Project description
```
