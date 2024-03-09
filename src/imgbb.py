import requests
import os

def upload(img_filename: str) -> str:
    print(f"Attempting to upload {img_filename} to freeimage.host")

    url = 'https://api.imgbb.com/1/upload'

    with open(img_filename, "rb") as file:
        
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
        print(f"Uploaded {img_filename} successfully to imgbb.com")
        try:
            image_url = r.json()['data']['url']
        
        except KeyError:
            raise ValueError(f"imgbb.com response malformed: {r.json()}")
        
        print("Image URL:", image_url)
        

    else:
        print(f"Failed to upload {img_filename} to imgbb.com, Status code: {r.status_code}")
        
    return image_url