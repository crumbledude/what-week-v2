import os
from io import BytesIO
import json
import requests

from datetime import datetime, timedelta
from unicodedata import normalize

from utils import background_img_fetch, image_process


def calculate_week_no() -> str:
    now = datetime.now()
    then = now + timedelta(days=3)
    then = then.strftime("%d-%m-%y")
    with open("../weeks.json", "r") as f:
        weekdict = json.load(f)
    try:
        return weekdict[then]
    except KeyError:
        print("Week not found in weeks.json, must be holiday. Exiting.")
        return None


def download_image(url) -> BytesIO:
    r = requests.get(url, timeout=60, allow_redirects=True)
    return BytesIO(r.content)


def main():
    print("Generating image...")
    week_no = calculate_week_no()

    if week_no is None:
        raise ValueError("Week number not found in weeks.json, must be holiday.")

    image_json = background_img_fetch.get_image()
    author = image_json["user"]["name"]
    author = normalize("NFKD", author).encode("ascii", "ignore").decode("utf-8")

    image_bytes = download_image(image_json["urls"]["regular"])

    caption = f"On Monday it will be week {week_no} at THS. The image is by {author} on Unsplash."

    # include elliot's instagram handle if the image is by him
    if author == "Elliot Crane":
        caption = caption[:-1] + " and @elliot_photography07 on instagram."

    image_process.lovely_art(image_bytes, week_no, author)

    with open("./web/data.json", "w", encoding="utf-8") as f:
        json.dump({"week": week_no, "author": author, "caption": caption}, f)


if __name__ == "__main__":
    main()
