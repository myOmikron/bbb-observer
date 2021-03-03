import json
import logging

import urllib3
import requests
import redis
import staticconfig
from staticconfig import Namespace


logger = logging.getLogger(__name__)


class Config(staticconfig.Config):

    def __init__(self):
        super().__init__()
        self.redis = Namespace()
        self.redis.host = "localhost"
        self.redis.port = 6379
        self.redis.db = 0

        self.events = ["MeetingEndingEvtMsg"]
        self.url = "change_me"
        self.verify_ssl_certs = True

        self.logging_level = logging.INFO


def main():
    config = Config.from_json("config.json")
    if not config.verify_ssl_certs:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    logging.basicConfig(level=config.logging_level)

    def receive(obj):
        message: dict = json.loads(obj["data"].decode())
        try:
            header = message["core"]["header"]
            logger.debug(f"Received redis message:\n{message['core']}")
            assert header["name"]
        except KeyError:
            logger.error("Malformed redis message: "+str(message))
            return

        if header["name"] in config.events:
            requests.post(config.url, json=message["core"], verify=config.verify_ssl_certs)
        else:
            logger.debug("Event '"+str(header["name"])+"' has no handler")

    connection = redis.Redis(**config.redis)
    pubsub = connection.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe(**{"from-akka-apps-redis-channel": receive})

    pubsub.run_in_thread(0.001).join()


if __name__ == "__main__":
    main()
