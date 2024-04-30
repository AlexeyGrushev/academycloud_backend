from app.config.worker import celery

if __name__ == "__main__":
    worker = celery.Worker()
    worker.start()
