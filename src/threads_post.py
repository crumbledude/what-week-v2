import os
import time
import requests

THREADS_USER_ID = os.getenv("THREADS_USER_ID")
THREADS_ACCESS_TOKEN = os.getenv("THREADS_ACCESS_TOKEN")

ENDPOINT = f"https://graph.threads.net/v1.0/{THREADS_USER_ID}"


def create_media_container(image_url):
    response = requests.post(f"{ENDPOINT}/threads",
                             params={
                                 "image_url": image_url,
                                 "media_type": "IMAGE",
                                 "access_token": THREADS_ACCESS_TOKEN,
                             },
                             timeout=30
    )

    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Failed to create media container: {response.json()}")

    time.sleep(30)

    # "It is recommended to wait on average 30 seconds before publishing a Threads media container
    # to give our server enough time to fully process the upload."

    return response.json()["id"]

def publish_media_container(media_id):
    response = requests.post(f"{ENDPOINT}/threads_publish",
                             params={
                                 "creation_id": media_id,
                                 "access_token": THREADS_ACCESS_TOKEN
                             },
                             timeout=30
    )

    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Failed to publish media container: {response.json()}")

    return response.json()
