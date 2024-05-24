import os
import cv2
import uuid
import asyncio
import logging
import threading
import numpy as np
from io import BytesIO
from db import Supabase
from typing import Dict

import face_recognition

from datetime import datetime
from dotenv import load_dotenv
from urllib.parse import urlparse
from realtime.connection import Socket

load_dotenv()

DEBUG = True
KILL_ALL = False

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
DATASET_BUCKET_NAME = os.getenv("DATASET_BUCKET_NAME")
CAMERA_LOG_BUCKET_NAME = os.getenv("CAMERA_LOG_BUCKET_NAME")

LOGGER = logging.getLogger(__name__)

ATTENDANCE_DB = []
ATTENDANCE_CACHE = {}
START_TRAINING_MODEL = False

lock = threading.Lock()
database = Supabase(SUPABASE_URL, SUPABASE_KEY)


def db_attendance_listener():
    global ATTENDANCE_DB

    while not KILL_ALL:
        if ATTENDANCE_DB:
            matches, frame_bytes = ATTENDANCE_DB.pop()
            for match in matches:
                id, known = match["id"], match["known"]
                cached_attendance = ATTENDANCE_CACHE.get(id)
                if (
                    not cached_attendance
                    or (datetime.now() - cached_attendance).total_seconds() > 60
                ):
                    try:
                        if known:
                            database.mark_attendance(
                                id, frame_bytes, CAMERA_LOG_BUCKET_NAME
                            )
                            LOGGER.info(f"Marked attendance for user {id}")
                            # Led green
                        else:
                            database.mark_unknown(
                                id, frame_bytes, CAMERA_LOG_BUCKET_NAME
                            )
                            LOGGER.info(f"Marked unknown for user {id}")
                            # led red

                    except Exception as E:
                        LOGGER.error("Failed to insert to db: ", E)

                    ATTENDANCE_CACHE[id] = datetime.now()


def model_training_listener():
    def callback(payload):
        global START_TRAINING_MODEL
        LOGGER.info("Received training event")
        with lock:
            START_TRAINING_MODEL = True

    asyncio.set_event_loop(asyncio.new_event_loop())
    realtime_listener = Socket(
        f"wss://{urlparse(SUPABASE_URL).netloc}/realtime/v1/websocket?apikey={SUPABASE_KEY}&vsn=1.0.0"
    )
    realtime_listener.connect()
    channel_1 = realtime_listener.set_channel("realtime:*")
    channel_1.join().on("INSERT", callback)
    callback("initial train")
    LOGGER.info("Preparing model training worker")
    realtime_listener.listen()


def detect_faces(encodings_storage: Dict, numpy_image_data):
    result = []

    if len(encodings_storage.keys()) == 0:
        return result

    confidence_threshold = 0.65  # Tailor as needed
    face_locations = face_recognition.face_locations(numpy_image_data)
    face_encodings = face_recognition.face_encodings(numpy_image_data, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        found_match = False

        for id, known_encodings in encodings_storage.items():
            distances = face_recognition.face_distance(known_encodings, face_encoding)
            min_distance = min(distances)

            if min_distance <= confidence_threshold:
                found_match = True
                result.append(
                    {
                        "id": id,
                        "location": face_location,
                        "known": not id.startswith("unknown"),
                    }
                )
                break

        if not found_match:
            unknown = {
                "id": f"unknown-{uuid.uuid4()}",
                "location": face_location,
                "known": False,
            }
            encodings_storage[unknown["id"]] = [face_encoding]
            result.append(unknown)

    return result


def fetch_train_dataset():
    global START_TRAINING_MODEL

    trained_dataset = {}
    dataset = database.fetch_dataset(DATASET_BUCKET_NAME)
    for user_id, user_faces in dataset.items():
        for image_bytes in user_faces:
            image_ = face_recognition.load_image_file(BytesIO(image_bytes))
            face_encodings = face_recognition.face_encodings(image_)

            if not face_encodings:
                continue

            trained_dataset.setdefault(user_id, []).extend(face_encodings)
    return trained_dataset


def face_recognition_listener():
    global ATTENDANCE_DB
    global START_TRAINING_MODEL

    video_feed = cv2.VideoCapture(0)

    FACE_ENCODINGS_STORAGE = {}

    while not KILL_ALL:
        try:
            ret, frame = video_feed.read()

            if not ret:
                LOGGER.error("No frame captured from video feed")
                break

            if START_TRAINING_MODEL:
                black_image = np.zeros_like(frame)

                (text_width, text_height), _ = cv2.getTextSize(
                    "Model is training for new faces", cv2.FONT_HERSHEY_SIMPLEX, 1, 2
                )

                center_x = black_image.shape[1] // 2
                center_y = black_image.shape[0] // 2 + text_height // 2

                cv2.putText(
                    black_image,
                    "Model is training for new faces",
                    (center_x - text_width // 2, center_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA,
                )
                cv2.imshow("Video", black_image)
                cv2.waitKey(1000)

                with lock:
                    FACE_ENCODINGS_STORAGE = fetch_train_dataset()
                    START_TRAINING_MODEL = False

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

            matches = detect_faces(FACE_ENCODINGS_STORAGE, rgb_small_frame)

            if matches:
                ATTENDANCE_DB.append(
                    (matches, cv2.imencode(".png", frame)[1].tobytes())
                )

            if DEBUG:
                # Show rectangle
                for face in matches:
                    id, location = face["id"], face["location"]
                    (top, right, bottom, left) = location
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.rectangle(
                        frame,
                        (left, bottom - 35),
                        (right, bottom),
                        (0, 0, 255),
                        cv2.FILLED,
                    )
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(
                        frame, id, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1
                    )
            cv2.imshow("Video", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        except Exception as e:
            print("error", e)
            LOGGER.error(e)

    video_feed.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    threading.Thread(target=model_training_listener, daemon=True).start()
    threading.Thread(target=db_attendance_listener, daemon=True).start()
    face_recognition_listener()
