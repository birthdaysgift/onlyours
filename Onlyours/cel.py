import os
from celery import Celery
import amqp

os.environ.setdefault("FORKED_BY_MULTIPROCESSING", "1")
app = Celery(
    "Onlyours",
    broker="amqp://myuser:mypassword@localhost:5672/myvhost"
)


@app.task
def upload_video():
    file = open("celery.txt", "w")
    file.write("Test upload video")
    file.close()


if __name__ == "__main__":
    app.start()
