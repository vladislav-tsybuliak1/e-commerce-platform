from fastapi import HTTPException, status

from core.schemas.product import ProductBase


def validate_product_stock_unit(product_create_update: ProductBase):
    if product_create_update.weight_product and product_create_update.stock_unit in ("PCS", "BOX"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Weight product unit should be 'KG', 'G', 'L', or 'ML'"
        )
