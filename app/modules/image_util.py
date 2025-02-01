from io import BytesIO
from flask import send_file
import numpy as np
from PIL import Image
import torch

def serve_pil_image(pil_img):
    # Create a BytesIO object to hold the image in memory
    img_io = BytesIO()

    # Save the PIL image as a JPEG to the BytesIO object
    pil_img.save(img_io, 'JPEG', quality=90)  # You can adjust the quality if needed
    img_io.seek(0)  # Move the cursor back to the beginning of the BytesIO object

    # Return the byte data of the JPEG image
    return send_file(BytesIO(img_io.getvalue()), mimetype='image/jpeg')


def convert_to_pil_image(img):
    if isinstance(img, np.ndarray):  # If it's a NumPy array
        return Image.fromarray(img)
    elif isinstance(img, torch.Tensor):  # If it's a PyTorch tensor
        img = img.cpu().numpy()  # Move to CPU and convert to NumPy
        return Image.fromarray(img)
    elif isinstance(img, Image.Image):  # If it's already a PIL Image
        return img
    else:
        raise TypeError(f"Unsupported image type: {type(img)}")
