from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from db import Base, Session, get_db
from datetime import datetime
from schemas.product import BaseProduct as SchemaBaseProduct
from schemas.product import Image as SchemaImage
from schemas.product import Product as SchemaProduct
from models.product import Product as ModelProduct
from models import product as ProductModel
from middleware.auth_middleware import auth_middleware
from uuid import uuid4
from urllib.parse import quote
from sqlalchemy.exc import IntegrityError
import os,boto3


router = APIRouter()

LIARA_ENDPOINT = os.getenv("LIARA_ENDPOINT")
LIARA_ACCESS_KEY = os.getenv("LIARA_ACCESS_KEY")
LIARA_SECRET_KEY = os.getenv("LIARA_SECRET_KEY")
LIARA_BUCKET_NAME = os.getenv("LIARA_BUCKET_NAME")

s3 = boto3.client(
    "s3",
    endpoint_url=LIARA_ENDPOINT,
    aws_access_key_id=LIARA_ACCESS_KEY,
    aws_secret_access_key=LIARA_SECRET_KEY,
)

@router.post("/product", response_model=SchemaProduct, status_code=201)
def create_product(product: SchemaBaseProduct, db: Session=Depends(get_db), auth_dict= Depends(auth_middleware)):
    
    if db.query(ModelProduct).filter(ModelProduct.product_code == product.product_code).first():
        raise HTTPException(status_code=409, detail="Duplicated product")
    product_id = str(uuid4())
    new_product = ModelProduct(id=product_id,
                               product_code=product.product_code,
                               name=product.name,
                               description=product.description,
                               category_id=product.category_id,
                               created_at=datetime.now().replace(second=0, microsecond=0))
    
    try:
        db.add(new_product)
        db.commit()
        return new_product
    except IntegrityError as e:
        db.rollback()
        if 'foreign key constraint' in str(e.orig):
            raise HTTPException(status_code=400, detail="Invalid category_id: does not exist in products_categories")
        else:
            raise HTTPException(status_code=500, detail="An error occurred while creating the product")

@router.get("/product/bycode/", response_model=SchemaProduct, status_code=200)
def get_product_by_code(product_code:str, db: Session=Depends(get_db)):
    product_db = db.query(ProductModel.Product).filter(ProductModel.Product.product_code == product_code).first()
    if not product_db:
        raise HTTPException(status_code=404, detail="product not found")
    else:
        return product_db

@router.post("/product/image", response_model=SchemaImage)
def post_image(product_code: str ,image: UploadFile=File(...), db: Session=Depends(get_db), auth_dict= Depends(auth_middleware)):
    image_id = str(uuid4())

    if not db.query(ModelProduct).filter(ModelProduct.product_code == product_code).first():
        raise HTTPException(status_code=404, detail=f"product with code {product_code} not found!")
    else:
        image_upload_res = s3.upload_fileobj(image.file, LIARA_BUCKET_NAME, f'sharksport/images/{image_id}.jpg')

        image_filename_encoded = quote(f'sharksport/images/{image_id}.jpg')
        image_permanent_url = f"https://{LIARA_BUCKET_NAME}.{LIARA_ENDPOINT.replace('https://', '')}/{image_filename_encoded}"

        new_image = ProductModel.Image(id=image_id,
                            url=image_permanent_url,
                            product_code= product_code,
                            created_at=datetime.now().replace(second=0, microsecond=0))

        db.add(new_image)
        db.commit()
        db.refresh(new_image)
        return new_image


@router.get("/product/images", status_code=200)
def get_prodcut_images(product_code: str, db: Session=Depends(get_db)):
    images = db.query(ProductModel.Image).filter(ProductModel.Image.product_code == product_code).all()

    return images



@router.delete("/product/images")
def delete_product_image(product_code: str, db: Session=Depends(get_db), auth_dict=Depends(auth_middleware)):
    db_image = db.query(ProductModel.Image).filter(ProductModel.Image.product_code == product_code).first()

    db.delete(db_image)
    db.commit()
    return db_image






@router.get("/product/list", status_code=200)
def get_product_list(db: Session=Depends(get_db)):
    return db.query(ModelProduct).filter(ModelProduct.deleted_at.is_(None)).first()







@router.patch("/product", response_model=SchemaProduct, status_code=200)
def update_product(product_code: str, patch_dict: SchemaBaseProduct, db: Session=Depends(get_db), auth_dict= Depends(auth_middleware)):
    
    if not db.query(ModelProduct).filter(ModelProduct.product_code == product_code).first():
        raise HTTPException(status_code=404, detail="Product not found!")
    
    product_model =  db.query(ModelProduct).filter(ModelProduct.product_code == product_code).first()

    product_model.product_code = patch_dict.product_code
    product_model.name = patch_dict.name
    product_model.description = patch_dict.description
    product_model.modified_at = datetime.now().replace(second=0, microsecond=0)

    db.commit()
    return product_model 





@router.delete("/product", response_model=SchemaProduct, status_code=200)
def product_soft_delete(product_code: str, db: Session=Depends(get_db), auth_dict= Session(auth_middleware)):
    if not db.query(ModelProduct).filter(ModelProduct.product_code == product_code).first():
        raise HTTPException(status_code=404,detail="Product not found!")
    
    delete_product = db.query(ModelProduct).filter(ModelProduct.product_code == product_code).first()

    delete_product.deleted_at = datetime.now().replace(second=0, microsecond=0)

    db.commit()
    return delete_product

    
