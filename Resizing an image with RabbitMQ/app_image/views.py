from django.shortcuts import render, redirect
from .models import UploadedImage
import pika
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        # save uploaded image to database
        uploaded = UploadedImage.objects.create(image=request.FILES["image"])

        # connect to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()

        # declare queue
        channel.queue_declare(queue="image_queue", durable=True)

        # send file path to queue
        message = {"id": uploaded.id, "file_path": uploaded.image.path}
        channel.basic_publish(
            exchange="",
            routing_key="image_queue",
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2),
        )

        connection.close()

        return redirect("upload")

    return render(request, "app_image/upload.html")
