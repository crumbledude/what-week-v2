import os
import time

import requests

WEB_URL = "url"


def create_instagram_container(image_url: str, caption: str) -> str:
    ig_user_id = os.environ["IG_USER_ID"]
    access_token = os.environ["IG_ACCESS_TOKEN"]

    r = requests.post(
        f"https://graph.facebook.com/v19.0/{ig_user_id}/media",
        timeout=60,
        params={
            "image_url": image_url,
            "caption": caption,
            "access_token": access_token,
        },
    )

    if r.status_code == 200:
        print(f"Uploaded {image_url} to instagram successfully")
        return r.json()["id"]

    else:
        print(
            f"Failed to upload {image_url} to instagram, Status code: {r.status_code}"
        )
        print(r.json())
        raise RuntimeError(
            f"Failed to upload {image_url} to instagram, Status code: {r.status_code}"
        )


def post_instagram_container(img_id):
    ig_user_id = os.environ["IG_USER_ID"]
    access_token = os.environ["IG_ACCESS_TOKEN"]

    r = requests.post(
        f"https://graph.facebook.com/v19.0/{ig_user_id}/media_publish",
        timeout=60,
        params={"creation_id": img_id, "access_token": access_token},
    )

    if r.status_code == 200:
        print(f"Published {img_id} to instagram successfully")

    else:
        print(f"Failed to publish {img_id} to instagram, Status code: {r.status_code}")
        print(r.json())
        raise RuntimeError(
            f"Failed to publish {img_id} to instagram, Status code: {r.status_code}"
        )


def request_data():
    r = requests.get(WEB_URL, timeout=60)

    if r.status_code != 200:
        print(f"Failed to fetch data from {WEB_URL}, Status code: {r.status_code}")
        print(r.json())
        raise RuntimeError(
            f"Failed to fetch data from {WEB_URL}, Status code: {r.status_code}"
        )

    return r.json()


if __name__ == "__main__":
    print("Posting to instagram")

    post_data = request_data()

    container_id = create_instagram_container(
        post_data["image_url"], post_data["caption"]
    )

    time.sleep(30)

    post_instagram_container(container_id)
