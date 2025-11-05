import os
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

MEDIA_PATH = "media/"

def upload_to_webp(instance, filename, folder="uploads"):
    base, ext = os.path.splitext(filename)
    filename_webp = f"{base}.webp"
    return os.path.join(folder, filename_webp)

def save_image_as_webp(image_field, folder="uploads"):
    if not image_field:
        return None

    img = Image.open(image_field)
    img = img.convert("RGB")  
    buffer = BytesIO()
    img.save(buffer, format="WEBP", quality=90)
    buffer.seek(0)
    return ContentFile(buffer.read())
