import requests

print("Please generate a short lived token for your account from:")
print("https://developers.facebook.com/tools/explorer/")
print("make sure you select the following permissions:")
print("pages_show_list, ads_management, business_management, instagram_basic, instagram_content_publish, pages_read_engagement, public_profile")
print("")
input("Press Enter to continue...")
token = input("Paste the token here and press enter: ")# stores the token in a variable


APP_ID = input("Enter your app id: ")
APP_SECRET = input("Enter your app secret: ")

def get_json(server):
    r = requests.post(server)

    if r.status_code == 200:
        return r
    else:
        print(r.status_code)
        raise KeyboardInterrupt

def save_token_start(token, time):
    with open("token_start.txt", "w") as f:
        f.write()

url = f"https://graph.facebook.com/v15.0/oauth/access_token?grant_type=fb_exchange_token&client_id={APP_ID}&client_secret={APP_SECRET}&fb_exchange_token={token}"
response = get_json(url).json()

print(response, "\n\n")

print("Long life token:", response["access_token"])