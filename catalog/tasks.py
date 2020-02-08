from celery.decorators import task

@task(name="add")
def add():
    print("Hello")
    return True