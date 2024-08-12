import requests

print("Please generate a short lived token for your account from:")
print("https://developers.facebook.com/tools/explorer/")
print("make sure you select the following permissions:")
print(
    "pages_show_list, ads_management, business_management, instagram_basic, instagram_content_publish, pages_read_engagement, public_profile"
)
print("")
input("Press Enter to continue...")
token = input("Paste the token here and press enter: ")


APP_SECRET = input("Enter your app secret: ")


def get_req(server):
    r = requests.get(server)

    if r.status_code == 200:
        return r
    else:
        print(r.status_code)

        try:
            print(r.json())
        except:
            pass

        raise KeyboardInterrupt


def save_token_start(token, time):
    with open("token_start.txt", "w") as f:
        f.write()


url = f"https://graph.threads.net/access_token?grant_type=th_exchange_token&client_secret={APP_SECRET}&access_token={token}"
response = get_req(url).json()

print(response, "\n\n")

print("Long life token:", response["access_token"])
