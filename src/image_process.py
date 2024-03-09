from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from datetime import datetime, timedelta

def lovely_art(img_bytes, week_number, author_name):
    img = Image.open(img_bytes)
    
    #crop image to 1:1 aspect ratio
    width, height = img.size
    resize = min(width, height)
    left = (width - resize)/2
    top = (height - resize)/2
    right = (width + resize)/2
    bottom = (height + resize)/2
    img = img.crop((left, top, right, bottom))
    
    #resize image to 1448x1448 to ensure font size is correct
    img = img.resize((1448, 1448))
    
    enhancer = ImageEnhance.Brightness(img)
    
    # to reduce brightness by 50%, use factor 0.5
    img = enhancer.enhance(0.5)
    
    draw = ImageDraw.Draw(img)
    
    font = ImageFont.truetype("./fonts/Roboto-Bold.ttf", 290)#setup font for main text
    draw.text((724, 724), "Week " + str(week_number), anchor="mm",font=font)#add current week text centered
    
    font = ImageFont.truetype("./fonts/Roboto-Bold.ttf", 95)#setup font info text
    draw.text((724, 280), "On Monday it will be at THS:", anchor="mm", font=font)#add info text centered

    font = ImageFont.truetype("./fonts/Roboto-Bold.ttf", 95)#as of date text
    current_date = datetime.now().strftime("%d-%m-%y")
    draw.text((724, 1168), "As of " + str(current_date), anchor="mm", font=font)#add date text centered
    
    font = ImageFont.truetype("./fonts/Roboto-Bold.ttf", 30)#author text
    draw.text((724, 1400), "Image by " + author_name + " on Unsplash", anchor="mm", font=font)#add author text centered
    
    img.save("img.png")