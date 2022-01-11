import os
from PIL import Image
from flask import current_app
import uuid


def add_image(uploaded_image):
    filename = uploaded_image.filename
    ext = filename.split('.')[-1]

    storage_filename = str(uuid.uuid1()) + '.' + ext 
    filepath = os.path.join(os.path.dirname(os.path.abspath(__name__)), 'static/images', storage_filename)

    output_size = (400, 400)
    image = Image.open(uploaded_image)
    image.thumbnail(output_size)
    image.save(filepath)

    return storage_filename