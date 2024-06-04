import base64

images = ["puman.png"]
encoded_images = {}

for image in images:
    with open(image, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        encoded_images[image] = encoded_string

with open("ico.py", "w") as output_file:
    output_file.write("encoded_images = " + str(encoded_images))
