from io import BytesIO
import os
import PIL
import PIL.Image
from dotenv import load_dotenv
from realtime.connection import Socket
from urllib.parse import urlparse
from redis_dict import RedisDict
from utils.db import create_client
import face_recognition
import numpy as np
import base64

from utils.redis import ProcessCommunication 

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SUPABASE_CLIENT = create_client(SUPABASE_URL, SUPABASE_KEY)

REDIS_DATASET = ProcessCommunication()


def callback1(payload):
    print("Callback 1: ", payload['record'])
    REDIS_DATASET.start_training()
    print(REDIS_DATASET.get_control_commands())


def get_domain(url):
    url = urlparse(url)
    return url.netloc


if __name__ == "__main__":
    
    URL = f"wss://{get_domain(SUPABASE_URL)}/realtime/v1/websocket?apikey={SUPABASE_KEY}&vsn=1.0.0"
    s = Socket(URL)
    s.connect()

    channel_1 = s.set_channel("realtime:*")
    channel_1.join().on("UPDATE", callback1)
    s.listen()