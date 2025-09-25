🖼️ Django + RabbitMQ Image Resizing Project  
 This project demonstrates how to integrate Django with RabbitMQ to handle background image processing without blocking the main application.  

🔹 Workflow:  
 A user uploads an image through the Django web app.  
 Instead of processing the image immediately, Django stores the file path in a RabbitMQ queue.  
 A worker service listens to the queue, retrieves the file path, and performs image processing (resizing, compression, etc.).  
 The processed image is saved back to the system, ready for further use.  

⚡ Why RabbitMQ?  
 Keeps the web app fast and responsive by delegating heavy tasks to background workers.  
 Ensures scalability when multiple users upload large files simultaneously.  
 Decouples the web layer from the processing layer, improving maintainability.  
 This setup is a practical example of asynchronous task processing in real-world applications like media platforms, e-commerce, and content management systems.  

▶️ Run the project

## Run RabbitMQ:

```
docker run -d --hostname rabbit --name rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management
# Management: http://localhost:15672 (guest/guest)
```

## Run the worker:
```
python worker.py
```

## Run Django:
```
python manage.py runserver
```
