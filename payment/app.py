from flask import Flask
import pika
import redis
import threading

app = Flask(__name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def process_order(ch, method, properties, body):
    order_id = body.decode()
    print(f"Processing order {order_id}")
    redis_client.set(order_id, "paid")

def start_rabbitmq_consumer():
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='orders')
    channel.basic_consume(queue='orders', on_message_callback=process_order, auto_ack=True)
    channel.start_consuming()

# Run RabbitMQ consumer in a separate thread
rabbitmq_thread = threading.Thread(target=start_rabbitmq_consumer)
rabbitmq_thread.daemon = True  # This ensures the thread will exit when the main program exits
rabbitmq_thread.start()

@app.route('/')
def home():
    return "Hello, RabbitMQ consumer is running in the background!"

if __name__ == "__main__":
    app.run(port=5000)
