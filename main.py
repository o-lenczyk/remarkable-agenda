from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageEnhance
import codecs
from cairosvg import svg2png

svg_img = open("meteogram.svg", "rt").read()
svg2png(bytestring=svg_img, write_to="meteogram.png")

f = codecs.open("agenda.txt", "r", "utf-8")

background = Image.new("RGB", (1404, 1872), color="white")
meteogram = Image.open("meteogram.png").convert("L")
enhancer = ImageEnhance.Sharpness(meteogram)
meteogram = enhancer.enhance(2)

font = ImageFont.truetype("DejaVuSansMono.ttf", 35)
d = ImageDraw.Draw(background)
d.text((20, 20), f.read(), fill=(0, 0, 0), font=font)

meteogram = meteogram.resize((1404, 702))
background.paste(meteogram, (0, 1160))

background.save("agenda.png")
