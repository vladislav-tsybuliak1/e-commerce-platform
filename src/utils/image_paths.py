import os
import uuid

from core.models import Product
from utils.slugify import slugify


def product_image_file_path(product: Product, filename: str) -> str:
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(product.name)}-{uuid.uuid4()}{extension}"
    return os.path.join("uploads/products/", filename)
