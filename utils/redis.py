from datetime import datetime
from redis_dict import RedisDict


class ProcessCommunication:

    def __init__(self, namespace="process-communication"):
        self.redis_dict = RedisDict(namespace=namespace)
        self.redis_dict = {"test": "tooo"}
        self.redis_dict.setdefault("attendance", {})
        self.redis_dict.setdefault(
            "controls",
            {
                "train-model": {"target": None, "run": False},
                "stop": False,
                "kill": False,
            },
        )

    def start_recognition(self):
        self.redis_dict["controls"]["stop"] = True

    def stop_recognition(self):
        self.redis_dict["controls"]["stop"] = True

    def get_control_commands(self):
        return self.redis_dict.get("controls")

    def start_training(self, target_id=None):
        self.redis_dict["controls"]["train-model"] = {
            "run": True,
            "target": target_id,
        }

    def model_training_status(self):
        return self.redis_dict["controls"]["train-model"]

    def get_last_attendance(self, user_id):
        return self.redis_dict["attendance"].get(user_id)

    async def stop_training(self):
        self.redis_dict["controls"]["train-model"] = {
            "run": False,
            "target": None,
        }

    async def model_training_ended(self, target_id=None):
        self.redis_dict["controls"]["train-model"] = {"target": target_id, "run": True}

    async def cache_last_attendance(self, user_id):
        self.redis_dict["attendance"][user_id] = datetime.now()
