from fastapi import HTTPException, status, UploadFile

from core.models import Product
from core.schemas.product import ProductBase


def validate_product_stock_unit(product_create_update: ProductBase):
    if product_create_update.weight_product and product_create_update.stock_unit in ("PCS", "BOX"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Weight product unit should be 'KG', 'G', 'L', or 'ML'"
        )


def validate_image_content_type(image: UploadFile):
    if image.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only png, jpeg, and jpg are allowed.",
        )

def validate_product_has_image(product: Product):
    if not product.image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product does not have image.",
        )
