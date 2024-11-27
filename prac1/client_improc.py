import xmlrpc.client
import base64
from PIL import Image
from io import BytesIO

# File paths
input_image_path = "chill.png"  # Replace with your input image filename
output_image_path = "grayscale_image.png"

# Connect to the server
proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

# Read the input image and encode it to base64
with open(input_image_path, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

# Send the image to the server and get the grayscale version
encoded_gray_image = proxy.convert_to_grayscale(encoded_image)

# Decode the received image and save it locally
gray_image_data = base64.b64decode(encoded_gray_image)
gray_image = Image.open(BytesIO(gray_image_data))
gray_image.save(output_image_path)

print(f"Grayscale image saved to {output_image_path}")
