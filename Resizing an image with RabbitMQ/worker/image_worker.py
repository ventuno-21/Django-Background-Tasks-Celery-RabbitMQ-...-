import json
import os
import sys

import django
import pika
from PIL import Image


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "a_config.settings")
django.setup()

from app_image.models import UploadedImage


def process_image(file_path):
    """Resize the image to 300x300 and save"""
    img = Image.open(file_path)
    img = img.resize((300, 300))

    # build new path inside media/processed
    base_dir = os.path.dirname(file_path)  # media/uploads
    filename = os.path.basename(file_path)  # Blogging-Platforms.jpeg
    processed_dir = base_dir.replace("uploads", "processed")

    os.makedirs(processed_dir, exist_ok=True)
    new_path = os.path.join(processed_dir, filename)

    img.save(new_path)
    return new_path


def callback(ch, method, properties, body):
    data = json.loads(body)
    print("📥 Received:", data)

    # process image
    new_path = process_image(data["file_path"])

    # update database with processed image path
    obj = UploadedImage.objects.get(id=data["id"])

    # make relative path properly (cross-platform)
    from django.conf import settings

    relative_path = os.path.relpath(new_path, settings.MEDIA_ROOT)

    obj.processed_image = relative_path
    obj.save()

    print("✅ Processed image saved:", new_path)
    ch.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="image_queue", durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="image_queue", on_message_callback=callback)

print("🚀 Worker started...")
channel.start_consuming()
