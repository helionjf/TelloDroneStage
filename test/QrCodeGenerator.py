import qrcode
from PIL import Image

# permet de créer un qrcode avec un string

img = qrcode.make('flip b')
img.save("flipb.png")
