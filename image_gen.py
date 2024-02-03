import os 
import json
import datetime
import requests
from random import choice
import PIL



def main():
    # imagejson = get_image()
    # image = imagejson["urls"]["regular"]
    # image_author = imagejson["user"]["name"]
    # download_image(image)
    # print(f"{image} by {image_author}")
    pass





#Get image from unsplash using a random search term and return a json file
def get_image():
    SEARCH_TERMS = ["red geometric pattern", "orange geometric pattern", "yellow geometric pattern", "green geometric pattern", "blue geometric pattern", "pink geometric pattern", "purple geometric pattern", "black geometric pattern"]

    response = requests.get("https://api.unsplash.com/photos/random",
            params={
            "client_id": os.getenv("UNSPLASH_ACCESS_TOKEN"),
            "query": (search_term := choice(SEARCH_TERMS)),
            "orientation": "squarish",
            "content_filter": "high"
        }
    )

    print("Getting picture using search term:", search_term)

    try:
        res_json = response.json()
        print("Successfully got image from Unsplash API.")

    except json.decoder.JSONDecodeError:
        print("Unsplash API response was not valid JSON.")
        exit()

    if response.status_code != 200:
        print(f"Unsplash API responded with status code {response.status_code} and error message: {res_json['errors'][0]}.")
        exit()

    return res_json


#Downloads the image
def download_image(url):
    r = requests.get(url, allow_redirects=True)
    open("image.jpeg", "wb").write(r.content)





if __name__ == "__main__":
    main()