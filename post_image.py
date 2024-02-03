import os
import requests
import base64
import json


#upload image to freeimage hosting

for file in os.listdir('.'):
    if file.endswith("_img.png"):
        img_file = file
        break
    
if not img_file:
    raise FileNotFoundError("No image file found")


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
    
    print(image_url)
    

else:
    print(f"Failed to upload {img_file} to imgbb.com, Status code: {r.status_code}")

# ----------------------------
# upload to instagram
ig_user_id = os.environ['IG_USER_ID']
access_token = os.environ['IG_ACCESS_TOKEN']

# create container

r = requests.post(
    f"https://graph.facebook.com/v19.0/{ig_user_id}/media",
    params={
        "image_url": image_url,
        "caption": "Test caption",
        "access_token": access_token
    }

if r.status_code == 200:
    print(f"Uploaded {img_file} to instagram successfully")
    img_id = r.json()['id']
    
else:
    print(f"Failed to upload {img_file} to instagram, Status code: {r.status_code}")
    print(r.json())

# publish container

r = requests.post(
    f"https://graph.facebook.com/v19.0/{ig_user_id}/media_publish",
    params={
        "creation_id": img_id,
        "access_token": access_token
    }
)

if r.status_code == 200:
    print(f"Published {img_file} to instagram successfully")
    
else:
    print(f"Failed to publish {img_file} to instagram, Status code: {r.status_code}")
    print(r.json())

