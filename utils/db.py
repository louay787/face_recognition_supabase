import logging
import uuid
from supabase import create_client

LOGGER = logging.getLogger(__name__)


class Supabase:

    def __init__(self, supabase_url, supabase_key):
        self._client = create_client(supabase_url, supabase_key)

    def upload_camera_logs_with_signed_url(
        self, file_name, image_binary, bucket_name
    ):
        self._client.storage.from_(bucket_name).upload(
            file=image_binary,
            path=file_name,
            file_options={"content-type": "image/jpeg"},
        )
        sign_url = self._client.storage.from_(bucket_name).create_signed_url(
            file_name, 6000000
        )

        return sign_url["signedURL"] if "signedURL" in sign_url else None

    async def mark_attendance(self, user_id, captured_face, bucket_name):
        file_name = f"{user_id}/{uuid.uuid4().hex}"

        signed_url = self.upload_camera_logs_with_signed_url(
            file_name, captured_face, bucket_name
        )
        data, _ = (
            self._client.table("attendance")
            .insert(
                {"user_id": user_id, "known": True, "camera_log_picture": signed_url}
            )
            .execute()
        )

        if "error" in data:
            LOGGER.error("Failed to mark attendance: ", data["error"])

    async def mark_unknown(self, captured_face, bucket_name):
        file_name = f"unknown/{uuid.uuid4().hex}"
        signed_url = self.upload_camera_logs_with_signed_url(
            file_name, captured_face, bucket_name
        )
        data, _ = self._client.table("attendance").insert({"known": False, "camera_log_picture": signed_url}).execute()

        if "error" in data:
            LOGGER.error("Failed to mark unknown: ", data["error"])

    def fetch_dataset(self, bucket_name, folder=None):
        dataset = {}
        files = (
            [
                f"{folder}/{file['name']}"
                for file in self._client.storage.from_(bucket_name).list(folder)
            ]
            if folder
            else [
                f"{folder['name']}/{file['name']}"
                for folder in self._client.storage.from_(bucket_name).list()
                for file in self._client.storage.from_(bucket_name).list(folder["name"])
            ]
        )

        for file_path in files:
            user_id, _ = file_path.split("/")
            image_bytes = self._client.storage.from_(bucket_name).download(file_path)
            if image_bytes:
                dataset.setdefault(user_id, [image_bytes])

        return dataset
