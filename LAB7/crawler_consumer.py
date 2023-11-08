import pika
import sys
import threading
from tinydb import TinyDB

# Using the "extract_details" function from LAB3.
sys.path.append("/Users/air/Desktop/PR/Labs/")
from LAB3.homework import extract_details


def store_data():
    """Stores data in the tinydb database my_db.json"""

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()
    channel.queue_declare(queue='links_queue', durable=True)

    def callback(ch, method, properties, body):
        # Decode the url.
        url = body.decode()

        # Print the name of thread and its link.
        print(threading.current_thread().name + ": ", url)

        # Extract the data from the page with the function from LAB3.
        data = extract_details(url)

        # Insert the data.
        db_lock.acquire()
        db.insert(data)
        db_lock.release()

        # Acknowledge the message.
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # Process only one link at a time from the queue.
    channel.basic_qos(prefetch_count=1)

    # Wait for links in the queue.
    channel.basic_consume(queue='links_queue', on_message_callback=callback)
    channel.start_consuming()


if __name__ == '__main__':
    # Create or open the database
    db = TinyDB('LAB7/my_db.json')

    # Allows to insert in the db only by one thread at a time.
    db_lock = threading.Lock()

    # Create and start the threads
    num_threads = 5
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=store_data)
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish then go with the next of the program
    for thread in threads: 
        thread.join()

    db.close()