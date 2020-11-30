import discord
from PIL import ImageFont, ImageDraw, Image
import io

def generate_image_text(text):
    lst = text.split()
    text2=""
    nlinec=2
    c = 0
    for i in range(len(lst)):
        c+=len(lst[i])
        if c > 19:
            text2 += f"\n{lst[i]} "
            nlinec+=1
            c=0
        else:
            text2 += f"{lst[i]} "
    #print(nlinec)
    img = Image.new("RGB", (650, nlinec*30), (54, 57, 63))
    font = ImageFont.truetype("lib\CONSOLA.TTF", 30)
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), text2, font=font)
    #print(type(a))
    arr = io.BytesIO()
    img.save(arr, format='PNG')
    arr.seek(0)
    file = discord.File(arr, filename='file.png')
    return file