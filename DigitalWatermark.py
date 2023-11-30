from PIL import Image
import numpy as np
import tkinter as tk
from tkinter import filedialog


    
def encode_image(image_path, secret_image_path, output_path):
    # Open the cover image and secret image
    cover_image = Image.open(image_path)
    secret_image = Image.open(secret_image_path)

    # # Get the size of the cover image and secret image
    cover_size = cover_image.size
    secret_size = secret_image.size

    # # Print the size of the cover image and secret image
    print('Cover image size:', cover_size)
    print('Secret image size:', secret_size)


    if secret_image.size > cover_image.size:
        secret_image = secret_image.resize(cover_image.size)

    # # Convert the images to numpy arrays
    cover_array = np.array(cover_image)
    secret_array = np.array(secret_image)

    # Get the dimensions of the cover image and secret image
    cover_height, cover_width, cover_channels = cover_array.shape
    secret_height, secret_width, secret_channels = secret_array.shape

    # Make sure the cover image is large enough to hold the secret image
    if (cover_height < secret_height) or (cover_width < secret_width):
        raise ValueError('Cover image is not large enough to hold secret image')

    # Pad the secret image with zeros to match the dimensions of the cover image
    pad_height = cover_height - secret_height
    pad_width = cover_width - secret_width
    padded_secret_array = np.pad(secret_array, ((0, pad_height), (0, pad_width), (0, 0)), mode='constant')

    # Create the stego image by replacing the least significant bit of each pixel in the cover image
    stego_array = cover_array.copy()
    for i in range(cover_height):
        for j in range(cover_width):
            for k in range(cover_channels):
                cover_pixel = int(cover_array[i][j][k])
                secret_pixel = int(padded_secret_array[i][j][k])
                stego_pixel = (cover_pixel & 254) | (secret_pixel >> 7)
                stego_array[i][j][k] = stego_pixel

    # Convert the stego image array to an image and save it to the output path
    stego_image = Image.fromarray(stego_array.astype(np.uint8))
    stego_image.save(output_path)

def decode_image(stego_image_path, output_path):
    # Open the stego image
    stego_image = Image.open(stego_image_path)

    # Convert the stego image to a numpy array
    stego_array = np.array(stego_image)

    # Extract the secret image by taking the least significant bit of each pixel in the stego image
    secret_array = np.zeros_like(stego_array)
    for i in range(stego_array.shape[0]):
        for j in range(stego_array.shape[1]):
            for k in range(stego_array.shape[2]):
                stego_pixel = int(stego_array[i][j][k])
                secret_pixel = ((stego_pixel & 1) << 7)
                secret_array[i][j][k] = secret_pixel

    # Convert the secret image array to an image and save it to the output path
    secret_image = Image.fromarray(secret_array.astype(np.uint8))
    secret_image.save(output_path)

# Example1 usage ชัดน้อยที่สุด
# encode_image('cover_image.jpg', 'secret_image.jpg', 'stego_image.jpg')
# decode_image('stego_image.jpg', 'secret_image_decoded.jpg')

# Example2 ชัดที่สุด เห็นรูป Decode ชัด โดยการเปลี่ยนประเภท outputเป็น png
# encode_image('cover_image.jpg', 'secret_image.jpg', 'stego_image.png')
# decode_image('stego_image.png', 'secret_image_decoded.png')

# ชัดน้อยกว่า Example1
# encode_image('cover_image.jpeg', 'secret_image.jpg', 'stego_image.jpg')
# decode_image('stego_image.jpg', 'secret_image_decoded.png')

filename = ''
def browse_file():
    filename = filedialog.askopenfilename()
    print("Selected File is: ", filename)
    print(type(filename))
    



root = tk.Tk()

label = tk.Label(root, text="Welcome to the picture encoder program")

browsebutton = tk.Button(root, text="Browse Cover Image", command = browse_file)
encodeb = tk.Button(root, text="Encode", command = encode_image('C:\Users\msiW10\Desktop\Watermask_v1\cover_image.jpg', 'secret_image.jpg', 'stego_image.png'))

label.pack()
encodeb.pack()
browsebutton.pack()

root.mainloop()