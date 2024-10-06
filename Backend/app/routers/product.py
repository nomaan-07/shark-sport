from fastapi import APIRouter, Depends, HTTPException
from models import product_management
from db import Base, Session, get_db
from schemas import schema
from datetime import datetime
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

router = APIRouter()





@router.post("/products/", response_model=schema.ProductResponse)
def create_product(product: schema.ProductCreate, db: Session = Depends(get_db)):
    try:
        product_data = product.model_dump()
        db_product = product_management.Product(**product_data, created_at=datetime.now().replace(second=0, microsecond=0))

        db.add(db_product)
        db.commit()
        db.refresh(db_product)

        return db_product

    except IntegrityError:
        db.rollback() 
        raise HTTPException(status_code=409, detail="Product with this identifier already exists.")

    except SQLAlchemyError as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail="An error occurred while creating the product.")

    except Exception as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))



# Read all products
@router.get("/products/", response_model=list[schema.ProductResponse])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        products = db.query(product_management.Product).offset(skip).limit(limit).all()
        return products
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving products.")



# Read a single product
@router.get("/products/{product_id}", response_model=schema.ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    try:
        product = db.query(product_management.Product).filter(product_management.Product.id == product_id).first()
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the product.")



# Update a product
@router.put("/products/{product_id}", response_model=schema.ProductResponse)
def update_product(product_id: int, product: schema.ProductCreate, db: Session = Depends(get_db)):
    try:
        db_product = db.query(product_management.Product).filter(product_management.Product.id == product_id).first()
        if db_product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        
        for key, value in product.model_dump().items():
            setattr(db_product, key, value)

        db.commit()
        db.refresh(db_product)
        return db_product

    except IntegrityError:
        db.rollback()  
        raise HTTPException(status_code=400, detail="Product update failed due to integrity constraints.")

    except SQLAlchemyError as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail="An error occurred while updating the product.")
    

# Delete a product
@router.delete("/products/{product_id}", response_model=dict)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    try:
        db_product = db.query(product_management.Product).filter(product_management.Product.id == product_id).first()
        if db_product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        
        db.delete(db_product)
        db.commit()
        return {"message": "Product deleted successfully"}

    except SQLAlchemyError as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail="An error occurred while deleting the product.")