import requests
from random import choice
import json
import os

def get_image():
    if (img_json := get_elliot_background()) is not None:
        return img_json

    return get_random_image()

    
def get_random_image():
    print("Getting random picture from Unsplash API.")
    SEARCH_TERMS = ["red","orange", "yellow", "green", "blue", "pink", "purple", "black"]

    search_term = choice(SEARCH_TERMS) + " geometric pattern"
    
    response = requests.get("https://api.unsplash.com/photos/random",
                timeout=60,
                params={
                    "client_id": os.getenv("UNSPLASH_ACCESS_TOKEN"),
                    "query": (search_term),
                    "orientation": "squarish",
                    "content_filter": "high"
        }
    )

    print("Getting picture using search term:", search_term)
    if response.status_code != 200:
        print(f"Status code {response.status_code}.")
        exit()

    try:
        res_json = response.json()
        print(f"Successfully got image - {img["links"]["html"]} - from Unsplash API.")

    except json.decoder.JSONDecodeError:
        print("Unsplash API response was not valid JSON.")
        exit()


    return res_json

def get_elliot_background() -> dict:
    print("Getting picture from Elliot's Unsplash profile.")
    response = requests.get("https://api.unsplash.com/users/e_c_crane/photos",
                timeout=60,
                params={
                    "client_id": os.getenv("UNSPLASH_ACCESS_TOKEN"),
                    "order_by": "latest",
                    "username": "e_c_crane",
                    "per_page": "30"
        }
    )

    if response.status_code != 200:
        print(f"Status code {response.status_code}.")
        exit()
    
    try:
        res_json = response.json()
        print("Successfully got image from Unsplash API.")

    except json.decoder.JSONDecodeError:
        print("Unsplash API response was not valid JSON.")
        exit()

    
    already_used_images = get_used_images()
    for img in res_json:
        if img["id"] not in already_used_images:
            print(f'Using image {img["links"]["html"]} from unsplash')
            add_used_image(img["id"])
            return img
        
    return None

def get_used_images():
    try:
        with open("used_images.txt", "r") as f:
            return [line.strip() for line in f.readlines()]
    
    except FileNotFoundError:
        with open("used_images.txt", "w") as f:
            f.write("")
            return []

def add_used_image(image_id):
    with open("used_images.txt", "a") as f:
        f.write(image_id + "\n")
