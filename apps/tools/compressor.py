from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

def compress_image(image, quality):
    img = Image.open(image)
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        img = img.convert("RGBA")
    else:
        img = img.convert("RGB")
    img.thumbnail((800, 800))  
    img_io = BytesIO()
    img.save(img_io, format='WEBP', optimize=True, quality=quality)
    return ContentFile(img_io.getvalue(), name=image.name.rsplit('.', 1)[0] + '.webp')


# def compress_image(image, quality=85):
#     """
#     Compress an image and save it as a WEBP file.
    
#     Args:
#         image: InMemoryUploadedFile or file-like object.
#         quality: Integer (1-100) defining the quality of the output image.

#     Returns:
#         ContentFile: Compressed image in WEBP format.
#     """
#     try:
#         img = Image.open(image)

#         # Handle transparency for PNG/GIF or palette images
#         if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
#             img = img.convert("RGBA")
#         else:
#             img = img.convert("RGB")

#         # Resize the image to fit within 800x800 pixels while maintaining aspect ratio
#         img.thumbnail((800, 800))

#         # Save the image to a BytesIO object in WEBP format
#         img_io = BytesIO()
#         img.save(img_io, format="WEBP", optimize=True, quality=100)
#         img_io.seek(0)

#         # Generate a new name with .webp extension
#         new_name = f"{image.name.rsplit('.', 1)[0]}.webp"

#         return ContentFile(img_io.getvalue(), name=new_name)
#     except Exception as e:
#         # Log the exception or handle it as needed
#         print(f"Error compressing image: {e}")
#         raise
