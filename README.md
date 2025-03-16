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

## First Version

### Features Implemented:

1. **Auth Service**:
   - Implemented basic user registration using FastAPI.
   - Used JWT for token-based authentication to secure endpoints.
   - User credentials are stored in a PostgreSQL database.
   
2. **Product Service**:
   - Created a Django-based service to handle product management.
   - Added product listing, creation, and retrieval functionality.
   - Connected the service to a PostgreSQL database.
   - Integrated RabbitMQ to publish orders when a user makes a purchase.

3. **Payment Service**:
   - Developed a simple Flask-based service to process payments.
   - The service listens to messages from RabbitMQ, which contain order details.
   - Payment status is updated upon receiving the order message.

4. **RabbitMQ Integration**:
   - Used RabbitMQ to decouple services and handle communication between Product and Payment services.
   - Product Service sends messages with order details to the RabbitMQ queue, and Payment Service processes the orders.

5. **Service Architecture**:
   - Separated services into different applications: Auth, Product, and Payment services.
   - Each service has its own repository and database.

### Improvements and Future Plans:
- **Error handling**: To improve resilience, we need to add better error handling across services.
- **User interaction**: The next step is to add a simple front-end to enable users to interact with the system.
- **Authorization improvements**: Implement more robust authentication and authorization mechanisms, such as user roles and permissions.
- **Order history**: Add functionality to view past orders and payment statuses.
- **Testing**: Set up unit and integration tests for each microservice.
