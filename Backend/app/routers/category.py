from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from db import get_db, Session
from models import product as ProductModel
from schemas import product as SchemaProduct
from middleware.auth_middleware import auth_middleware


router = APIRouter()

@router.post("/categories", response_model=SchemaProduct.ProductCategory, status_code=201)
def create_category(category: SchemaProduct.BaseProductCategory, db: Session=Depends(get_db), auth_dict= Depends(auth_middleware)):
    
    if db.query(ProductModel.ProductCategory).filter(ProductModel.ProductCategory.id == category.id).first():
        raise HTTPException(status_code=409, detail="Duplicated category")

    new_category = ProductModel.ProductCategory(id=category.id,
                                   name=category.name,
                                   description=category.description,
                                   created_at=datetime.now().replace(second=0 , microsecond=0))
    
    

    db.add(new_category)
    db.commit()
    return new_category
    





@router.get("/categories", status_code=200)
def get_categories(db: Session=Depends(get_db)):
    categories = db.query(ProductModel.ProductCategory).filter(ProductModel.ProductCategory.deleted_at.is_(None)).all()

    return categories






@router.patch("/categories", response_model=SchemaProduct.ProductCategory, status_code=200)
def update_category(category: SchemaProduct.BaseProductCategory, id, db:Session=Depends(get_db)):
    update_category = db.query(ProductModel.ProductCategory).filter(ProductModel.ProductCategory.id == id).first()
    
    update_category.id = category.id
    update_category.name = category.name
    update_category.description = category.description
    update_category.modified_at = datetime.now().replace(second=0, microsecond=0)

    db.commit()
    return update_category







@router.delete("/categories", response_model=SchemaProduct.ProductCategory, status_code=200)
def soft_delete_category(category_id: str, db: Session=Depends(get_db)):
    dl_category = db.query(ProductModel.ProductCategory).filter(ProductModel.ProductCategory.id == category_id).first()

    dl_category.deleted_at = datetime.now().replace(second=0, microsecond=0)

    db.commit()
    return dl_category
