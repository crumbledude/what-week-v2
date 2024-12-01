import os 
import json
import requests
from random import choice
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from io import BytesIO
from datetime import datetime, timedelta
from unicodedata import normalize

def main():
    now = datetime.now()
    then = now + timedelta(days = 1)
    then = then.strftime("%d-%m-%y")
    with open("./weeks.json", "r") as f:
        weekdict = json.load(f)

    if then not in weekdict:
        exit()
    else:
        author = image_handler()
        
        caption = f"On Monday it will be week {calculate_week_no()} at THS. The image is by {author} on Unsplash."
        
        image_url = upload_to_imgbb("img.png")
        
        image_ID = create_instagram_container(image_url, caption)
        post_instagram_container(image_ID) 
    
#Get the image from unsplash and download it
def image_handler():
    imagejson = get_image()
    image = imagejson["urls"]["regular"]
    image_author = imagejson["user"]["name"]
    nice_img_auth = normalize('NFKD', image_author).encode('ascii','ignore').decode('utf-8')
    
    img_bytes = download_image(image)
    
    lovely_art(img_bytes, calculate_week_no(), nice_img_auth)
    
    return image_author

#Get image from unsplash using a random search term and return a json file
def get_image():
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

    try:
        res_json = response.json()
        print("Successfully got image from Unsplash API.")

    except json.decoder.JSONDecodeError:
        print("Unsplash API response was not valid JSON.")
        exit()

    if response.status_code != 200:
        print(f"Status code {response.status_code} and error message: {res_json['errors'][0]}.")
        exit()

    return res_json

#Downloads the image
def download_image(url):
    r = requests.get(url, timeout=60, allow_redirects=True)
    return BytesIO(r.content)

def calculate_week_no():
    now = datetime.now()
    then = now + timedelta(days = 3)
    then = then.strftime("%d-%m-%y")
    with open("./weeks.json", "r") as f:
        weekdict = json.load(f)
    week = weekdict[then]
    return week

#Mangle the image and add text
def lovely_art(img_bytes, week_number, author_name):
    img = Image.open(img_bytes)
    img = img.resize((1448, 1448))
    
    enhancer = ImageEnhance.Brightness(img)
    
    # to reduce brightness by 50%, use factor 0.5
    img = enhancer.enhance(0.5)
    
    draw = ImageDraw.Draw(img)
    
    font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 290)#setup font for main text
    draw.text((724, 724), "Week " + str(week_number), anchor="mm",font=font)#add current week text centered
    
    font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 95)#setup font info text
    draw.text((724, 280), "On Monday it will be at THS:", anchor="mm", font=font)#add info text centered

    font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 95)#as of date text
    current_date = datetime.now().strftime("%d-%m-%y")
    draw.text((724, 1168), "As of " + str(current_date), anchor="mm", font=font)#add date text centered
    
    font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 30)#author text
    draw.text((724, 1400), "Image by " + author_name + " on Unsplash", anchor="mm", font=font)#add author text centered
    
    img.save("img.png")

#-------------------------------------------------------------------------------------------------------------------------------

def upload_to_imgbb(img_file):
    print(f"Attempting to upload {img_file} to freeimage.host")

    url = 'https://api.imgbb.com/1/upload'

    with open(img_file, "rb") as file:
        
        r = requests.post(url, timeout=60, 

            params={
                'expiration': 600,
                'key': os.environ['IMGBB_API_KEY'],
            },
            files={
                'image': file
            }
                            )

    if r.status_code == 200:
        print(f"Uploaded {img_file} successfully to imgbb.com")
        try:
            image_url = r.json()['data']['url']
        
        except KeyError:
            raise ValueError(f"imgbb.com response malformed: {r.json()}")
        
        print("Image URL:", image_url)
        

    else:
        print(f"Failed to upload {img_file} to imgbb.com, Status code: {r.status_code}")
        
    return image_url

def create_instagram_container(image_url, caption):
    ig_user_id = os.environ['IG_USER_ID']
    access_token = os.environ['IG_ACCESS_TOKEN']

    r = requests.post(
        f"https://graph.facebook.com/v19.0/{ig_user_id}/media",
        timeout=60,
        params={
            "image_url": image_url,
            "caption": caption,
            "access_token": access_token
        }
    )

    if r.status_code == 200:
        print(f"Uploaded {image_url} to instagram successfully")
        
        return r.json()['id']
        
    else:
        print(f"Failed to upload {image_url} to instagram, Status code: {r.status_code}")
        print(r.json())
        
        
def post_instagram_container(img_id):
    ig_user_id = os.environ['IG_USER_ID']
    access_token = os.environ['IG_ACCESS_TOKEN']

    r = requests.post(
        f"https://graph.facebook.com/v19.0/{ig_user_id}/media_publish",
        timeout=60,
        params={
            "creation_id": img_id,
            "access_token": access_token
        }
    )

    if r.status_code == 200:
        print(f"Published {img_id} to instagram successfully")
        
    else:
        print(f"Failed to publish {img_id} to instagram, Status code: {r.status_code}")
        print(r.json())
    
if __name__ == "__main__":
    main()
