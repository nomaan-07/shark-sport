"""from fastapi import APIRouter, HTTPException, Depends
from db import Session, get_db
from models import product as ModelProduct
from schemas import product as SchemaProduct
from datetime import datetime


router = APIRouter()

@router.post("/product/create", response_model=SchemaProduct.ProductCreate, status_code=201)
def create_product(product_info: SchemaProduct.ProductBase, db: Session=Depends(get_db)):
    product_data = product_info.model_dump()
    product = ModelProduct.Product(**product_data, created_at=datetime.now().replace(second=0, microsecond=0))

    db.add(product)
    db.commit()
    return product"""