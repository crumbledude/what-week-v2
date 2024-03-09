import os
from io import BytesIO
import json
import requests

from datetime import datetime, timedelta
from unicodedata import normalize

import ig
from image_process import lovely_art
from background_img_fetch import get_image
import imgbb

def main():
    week_no = calculate_week_no()
    
    image_json = get_image()
    author = image_json["user"]["name"]
    author = normalize('NFKD', author).encode('ascii','ignore').decode('utf-8')
    
    image_bytes = download_image(image_json["urls"]["regular"])
    
    caption = f"On Monday it will be week {calculate_week_no()} at THS. The image is by {author} on Unsplash."
    
    lovely_art(image_bytes, week_no, author)
    
    image_url = imgbb.upload("img.png")
    print(image_url)
    
    #tag Elliot if it's his image
    if author == "Elliot Crane":
        tags = [{"username": "elliot_photography07",
                "x": 0.48,
                "y": 0.96}]
    else:
        tags = False

    image_ID = ig.create_instagram_container(image_url, caption, tags)
    ig.post_instagram_container(image_ID) 

def download_image(url) -> bytes:
    r = requests.get(url, timeout=60, allow_redirects=True)
    return BytesIO(r.content)


def calculate_week_no()-> str:
    now = datetime.now()
    #ensure days is adjusted back to 3 in production
    then = now + timedelta(days = 2)
    then = then.strftime("%d-%m-%y")
    with open("./weeks.json", "r") as f:
        weekdict = json.load(f)
    try:
        return weekdict[then]
    except KeyError:
        print("Week not found in weeks.json, must be holiday. Exiting.")
        exit()

#-------------------------------------------------------------------------------------------------------------------------------


    
if __name__ == "__main__":
    main()