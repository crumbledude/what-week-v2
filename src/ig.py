import os
import requests

def create_instagram_container(image_url: str, caption: str, tags: dict) -> str:
    ig_user_id = os.environ['IG_USER_ID']
    access_token = os.environ['IG_ACCESS_TOKEN']

    params={
        "image_url": image_url,
        "caption": caption,
        "access_token": access_token
    }
    
    if tags:
        params["user_tags"] = tags
    
    r = requests.post(
        f"https://graph.facebook.com/v19.0/{ig_user_id}/media",
        timeout=60,
        params=params
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