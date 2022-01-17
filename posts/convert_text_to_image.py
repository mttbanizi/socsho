from PIL import Image, ImageDraw, ImageFont

# gfg_logo.jpeg image opened using open function and
# assigned to variable named img
img = Image.open('gfg_logo.jpeg')

# Image is converted into editable form using Draw
# function and assigned to d1
d1 = ImageDraw.Draw(img)

# Font selection from the downloaded file
myFont = ImageFont.truetype('/home/raghav/PycharmProjects/gfg/00006_44s.ttf', 30)

# Decide the text location, color and font
d1.text((0, 170), "Sample text", fill=(0, 255, 0), font=myFont)

# show and save the image
img.show()
img.save("results.jpeg")