"""
Kafka Service for LearnFlow
Handles event-driven communication between services
"""
from confluent_kafka import Producer, Consumer, KafkaException
import json
import logging
import asyncio
from typing import Dict, Any, Callable, Optional
from threading import Thread
import time

logger = logging.getLogger(__name__)

class KafkaService:
    def __init__(self, bootstrap_servers: str = "localhost:9092"):
        self.bootstrap_servers = bootstrap_servers
        self.producer = None
        self.consumer = None
        self.running = False

        # Configuration for producer
        self.producer_config = {
            'bootstrap.servers': bootstrap_servers,
            'acks': 'all',
            'enable.idempotence': True,
        }

        # Configuration for consumer
        self.consumer_config = {
            'bootstrap.servers': bootstrap_servers,
            'group.id': 'learnflow-group',
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': True,
        }

    def connect_producer(self):
        """Connect to Kafka producer"""
        try:
            self.producer = Producer(self.producer_config)
            logger.info("Connected to Kafka producer")
        except Exception as e:
            logger.error(f"Failed to connect to Kafka producer: {str(e)}")
            raise

    def connect_consumer(self):
        """Connect to Kafka consumer"""
        try:
            self.consumer = Consumer(self.consumer_config)
            logger.info("Connected to Kafka consumer")
        except Exception as e:
            logger.error(f"Failed to connect to Kafka consumer: {str(e)}")
            raise

    def delivery_callback(self, err, msg):
        """Callback for producer delivery reports"""
        if err is not None:
            logger.error(f'Message delivery failed: {err}')
        else:
            logger.info(f'Message delivered to {msg.topic()} [{msg.partition()}]')

    async def send_event(self, topic: str, event_data: Dict[str, Any], key: Optional[str] = None):
        """
        Send an event to a Kafka topic

        Args:
            topic: Kafka topic to send the event to
            event_data: Event data to send
            key: Optional key for partitioning
        """
        if not self.producer:
            self.connect_producer()

        try:
            # Serialize the event data
            serialized_data = json.dumps(event_data).encode('utf-8')

            # Produce the message
            self.producer.produce(
                topic=topic,
                key=key,
                value=serialized_data,
                callback=self.delivery_callback
            )

            # Wait for any outstanding messages to be delivered and delivery reports to be received
            self.producer.flush()

            logger.info(f"Event sent to topic {topic}")
        except Exception as e:
            logger.error(f"Failed to send event to topic {topic}: {str(e)}")
            raise

    def consume_events(self, topics: list, message_handler: Callable[[Dict[str, Any]], None]):
        """
        Consume events from Kafka topics

        Args:
            topics: List of topics to consume from
            message_handler: Function to handle received messages
        """
        if not self.consumer:
            self.connect_consumer()

        try:
            self.consumer.subscribe(topics)
            logger.info(f"Subscribed to topics: {topics}")

            while self.running:
                # Poll for messages
                msg = self.consumer.poll(timeout=1.0)

                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaException._PARTITION_EOF:
                        # End of partition event
                        continue
                    else:
                        logger.error(msg.error())
                        continue

                # Process the message
                try:
                    # Deserialize the message value
                    event_data = json.loads(msg.value().decode('utf-8'))

                    # Call the message handler
                    message_handler(event_data)

                    logger.info(f"Processed message from topic {msg.topic()}")
                except json.JSONDecodeError:
                    logger.error(f"Failed to decode JSON from message: {msg.value()}")
                except Exception as e:
                    logger.error(f"Error processing message: {str(e)}")

        except KeyboardInterrupt:
            logger.info("Consumer interrupted")
        finally:
            self.consumer.close()

    def start_consumer_thread(self, topics: list, message_handler: Callable[[Dict[str, Any]], None]):
        """
        Start consumer in a separate thread

        Args:
            topics: List of topics to consume from
            message_handler: Function to handle received messages
        """
        self.running = True
        consumer_thread = Thread(
            target=self.consume_events,
            args=(topics, message_handler),
            daemon=True
        )
        consumer_thread.start()
        return consumer_thread

    def stop_consumer(self):
        """Stop the consumer"""
        self.running = False

    async def send_user_interaction_event(self, user_id: str, interaction_type: str, data: Dict[str, Any]):
        """
        Send a user interaction event

        Args:
            user_id: ID of the user
            interaction_type: Type of interaction (e.g., 'code_run', 'lesson_completed', 'exercise_attempt')
            data: Additional data about the interaction
        """
        event = {
            "event_type": "user_interaction",
            "user_id": user_id,
            "interaction_type": interaction_type,
            "timestamp": time.time(),
            "data": data
        }

        await self.send_event("user-interactions", event, key=user_id)

    async def send_progress_update_event(self, user_id: str, progress_data: Dict[str, Any]):
        """
        Send a progress update event

        Args:
            user_id: ID of the user
            progress_data: Progress data to send
        """
        event = {
            "event_type": "progress_update",
            "user_id": user_id,
            "timestamp": time.time(),
            "progress_data": progress_data
        }

        await self.send_event("progress-updates", event, key=user_id)

    async def send_ai_interaction_event(self, user_id: str, query: str, response: str, agent_type: str):
        """
        Send an AI interaction event

        Args:
            user_id: ID of the user
            query: User's query to the AI
            response: AI's response
            agent_type: Type of AI agent that handled the request
        """
        event = {
            "event_type": "ai_interaction",
            "user_id": user_id,
            "query": query,
            "response": response,
            "agent_type": agent_type,
            "timestamp": time.time()
        }

        await self.send_event("ai-interactions", event, key=user_id)


# Global Kafka service instance
kafka_service = KafkaService()

async def init_kafka_service(bootstrap_servers: str = "localhost:9092"):
    """
    Initialize the Kafka service

    Args:
        bootstrap_servers: Kafka bootstrap servers
    """
    global kafka_service
    kafka_service = KafkaService(bootstrap_servers)

    # Connect the producer
    kafka_service.connect_producer()

    logger.info("Kafka service initialized")


async def send_user_interaction(user_id: str, interaction_type: str, data: Dict[str, Any]):
    """
    Convenience function to send a user interaction event

    Args:
        user_id: ID of the user
        interaction_type: Type of interaction
        data: Additional data
    """
    await kafka_service.send_user_interaction_event(user_id, interaction_type, data)


async def send_progress_update(user_id: str, progress_data: Dict[str, Any]):
    """
    Convenience function to send a progress update event

    Args:
        user_id: ID of the user
        progress_data: Progress data
    """
    await kafka_service.send_progress_update_event(user_id, progress_data)


async def send_ai_interaction(user_id: str, query: str, response: str, agent_type: str):
    """
    Convenience function to send an AI interaction event

    Args:
        user_id: ID of the user
        query: User's query
        response: AI's response
        agent_type: Type of AI agent
    """
    await kafka_service.send_ai_interaction_event(user_id, query, response, agent_type)