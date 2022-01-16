from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import codecs

f = codecs.open("agenda.txt", "r", "utf-8")

img = Image.new("RGB", (1404, 1872), color="white")

font = ImageFont.truetype("DejaVuSansMono.ttf", 35)
d = ImageDraw.Draw(img)
d.text((20, 20), f.read(), fill=(0, 0, 0), font=font)

img.save("agenda.png")
