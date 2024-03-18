import os 
from celery import Celery 

# set the default Django settings module for the 'celery' program. 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ailaysapro.settings')

app = Celery('ailaysa')


app.config_from_object('django.conf:settings',	namespace='CELERY')


app.autodiscover_tasks()

@app.task
def count_words_in_file(file_path):
    try:
        # Open the file and read its content
        with open(file_path, 'r') as file:
            content = file.read()

        # Count the number of words in the content
        word_count = len(content.split())

        return word_count
    except FileNotFoundError:
        # Handle file not found error
        return "File not found"
    except Exception as e:
        # Handle other exceptions
        return f"Error: {e}"