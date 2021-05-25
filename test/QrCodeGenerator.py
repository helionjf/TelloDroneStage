import qrcode

# permet de créer un qrcode avec un string

img = qrcode.make('Box n1 15kg computer')
img.save("Resources/Box1.png")
