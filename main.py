import asyncio
from datetime import datetime
import logging
import os
import cv2
import numpy as np

# from datetime import datetime
from dotenv import load_dotenv
from redis_dict import RedisDict
from utils import Recognition, Supabase
from utils.redis import ProcessCommunication

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
DATASET_BUCKET_NAME = os.getenv("DATASET_BUCKET_NAME")
CAMERA_LOG_BUCKET_NAME = os.getenv("CAMERA_LOG_BUCKET_NAME")

LOGGER = logging.getLogger(__name__)

recognition_model = Recognition()
database = Supabase(SUPABASE_URL, SUPABASE_KEY)


def debugging_highlight_recognized_faces(frame, faces):

    for face in faces:
        id, location = face["id"], face["location"]
        (top, right, bottom, left) = location
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        # Draw a box around the face

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(
            frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED
        )
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, id, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


async def start_training_model():
    dataset = database.fetch_dataset(DATASET_BUCKET_NAME)
    recognition_model.trained_dataset(dataset)


async def listen(debug=False):
    video_feed = cv2.VideoCapture(0)
    process_communication = ProcessCommunication()

    await start_training_model()

    while not process_communication.get_control_commands()["kill"]:

        commands = process_communication.get_control_commands()

        if commands["stop"]:
            continue

        if commands["train-model"]["run"]:
            await start_training_model(commands["train_model"]["target"])
            process_communication.stop_training()

        try:
            _, frame = video_feed.read()

            if frame is None:
                # Handle no frame read error (e.g., video ended)
                LOGGER.error("No frame captured from video feed")
                break

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

            matches = recognition_model.detect_faces(rgb_small_frame)

            for match in matches:
                id, known = match["id"], match["known"]
                if known:
                    cached_attendance = process_communication.get_last_attendance(id)

                    if (
                        not cached_attendance
                        or (datetime.now() - cached_attendance).total_seconds() > 60
                    ):
                        await process_communication.cache_last_attendance(id)
                        await database.mark_attendance(
                            id,
                            cv2.imencode(".png", frame)[1].tobytes(),
                            CAMERA_LOG_BUCKET_NAME,
                        )

                else:
                    # pass
                    await database.mark_unknown(
                        cv2.imencode(".png", frame)[1].tobytes(), CAMERA_LOG_BUCKET_NAME
                    )

        except Exception as e:
            LOGGER.error(e)

        if debug:
            debugging_highlight_recognized_faces(frame, matches)
            cv2.imshow("Video", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    video_feed.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    asyncio.run(listen(debug=True))
