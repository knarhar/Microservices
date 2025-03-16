from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
import pika, json, logging

logger = logging.getLogger(__name__)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        """ Save product and publish the event to RabbitMQ """
        product = serializer.save()
        self.publish_to_rabbitmq(product)

    @staticmethod
    def publish_to_rabbitmq(product):
        """ Publish product ID to RabbitMQ with better handling """
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()

            # Ensure the queue exists (should ideally be done once at startup)
            channel.queue_declare(queue='orders', durable=True)

            # Convert to JSON (better practice)
            message = json.dumps({"product_id": product.id})
            channel.basic_publish(
                exchange='',
                routing_key='orders',
                body=message,
                properties=pika.BasicProperties(delivery_mode=2)  # Makes message persistent
            )

            connection.close()
            logger.info(f"Published product {product.id} to RabbitMQ")

        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
        except Exception as e:
            logger.error(f"Error publishing message: {e}")
