from fastapi import APIRouter, HTTPException, Depends, UploadFile, Form, File
from db import Session, get_db, joinedload
from models import product as ModelProduct
from schemas import product as SchemaProduct
from tools import current_time, BucketObj
from middleware.auth_middleware import user_auth_middleware, admin_auth_middleware
import uuid




router = APIRouter(
    prefix="/product"
)
admin_router = APIRouter(
    prefix="/admin"
)

# Product
@router.get("/list/")
def read_products(db: Session = Depends(get_db)):
    return db.query(ModelProduct.Product).all()


@router.get("/get_product/{product_id}")
def read_product(product_id: str, db: Session = Depends(get_db)):
    product = db.query(ModelProduct.Product).filter(ModelProduct.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@admin_router.post("/create_product/", response_model=SchemaProduct.ProductCreated, status_code=201)
def create_product(product_info: SchemaProduct.ProductBase,
                   db: Session=Depends(get_db),
                   admin_auth=Depends(admin_auth_middleware)):
    if db.query(ModelProduct.Product).filter(ModelProduct.Product.name == product_info.name).first():
        raise HTTPException(status_code=404, detail="Duplicated product name")
    category = db.query(ModelProduct.ProductCategory).filter(ModelProduct.ProductCategory.id == product_info.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Product category not found")
    discount = db.query(ModelProduct.Discount).filter(ModelProduct.Discount.id == product_info.discount_id).first()
    new_price = product_info.original_price
    if  discount:
        new_price -= (new_price * discount.discount_rate / 100)
    else:
        new_price = product_info.original_price

    product_data = product_info.model_dump()
    new_product = ModelProduct.Product(
        id = f'{product_info.name}-{product_info.brand}-{current_time()}',
        **product_data,
        price_after_discount=new_price,
        created_at=current_time()  
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product) 

    return new_product
    


@admin_router.post("/product/create_images", status_code=201)
def create_product_images(images: list[UploadFile]=File(...), product_id: str=Form(...), db=Depends(get_db),
                          admin_auth=Depends(admin_auth_middleware)):
    return



# Category
@admin_router.post("/create_category",
              response_model=SchemaProduct.ProductCategoryCreate,
              status_code=201)
def create_category(category_info: SchemaProduct.ProductCategoryBase,
                    db: Session=Depends(get_db),
                    admin_auth=Depends(admin_auth_middleware)):
    if not db.query(ModelProduct.ProductCategory).filter(ModelProduct.ProductCategory.id == category_info.id).first():
        if not db.query(ModelProduct.ProductCategory).filter(ModelProduct.ProductCategory.name == category_info.name).first():
            info = category_info.model_dump()
            new_category = ModelProduct.ProductCategory(**info, created_at=current_time())
            db.add(new_category)
            db.commit()
            return new_category
    raise HTTPException(status_code=409, detail="duplicated category")



# Size
@admin_router.post("/create_size/", response_model=SchemaProduct.Size, status_code=201)
def create_size(size_info: SchemaProduct.SizeBase, db: Session=Depends(get_db),
                admin_auth=Depends(admin_auth_middleware)):
    
    if db.query(ModelProduct.Product).filter(ModelProduct.Product.id == size_info.product_id).first():
        info = size_info.model_dump()
        size_id =  f"{size_info.product_id}-{size_info.size}"
        new_size = ModelProduct.Size(**info, id=size_id ,modified_at= current_time())
        db.add(new_size)
        db.commit()
        return new_size
    
    raise HTTPException(status_code=400, detail="no product to asign size for")



# Discount
@admin_router.get("/discount_list/")
def discount_list(db: Session=Depends(get_db),
                  admin_auth=Depends(admin_auth_middleware)): #only admin should access
    return db.query(ModelProduct.Discount).all()


@admin_router.post("/create_discount", response_model=SchemaProduct.Discount, status_code=201)
def create_discound(discount_info: SchemaProduct.DiscountBase, db: Session=Depends(get_db),
                    admin_auth=Depends(admin_auth_middleware)):
    discount_db = db.query(ModelProduct.Discount).filter(ModelProduct.Discount.discount_code == discount_info.discount_code).first()
    if not discount_db :
        info = discount_info.model_dump()
        new_discount = ModelProduct.Discount(**info, id=f"{discount_info.discount_code}-{uuid.uuid4()}" ,created_at=current_time())
        db.add(new_discount)
        db.commit()
        return new_discount
    raise HTTPException(status_code=409, detail="Duplicated discount")
        


@admin_router.get("/reviews_list/", response_model=list, status_code=200)
def read_product_reviews(db: Session = Depends(get_db),
                         admin_auth=Depends(admin_auth_middleware)):
    return db.query(ModelProduct.ProductReview).all()

@admin_router.get("/get_reviews/{review_id}", response_model=SchemaProduct.ProductReview)
def read_product_review(review_id: str, db: Session = Depends(get_db),
                        admin_auth=Depends(admin_auth_middleware)):
    review = db.query(ModelProduct.ProductReview).filter(ModelProduct.ProductReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Product review not found")
    return review

@router.post("/product_reviews/")
def create_product_review(review: SchemaProduct.ProductReview, db: Session = Depends(get_db)):
    db.add(review)
    db.commit()
    return review

@router.put("/product_reviews/{review_id}")
def update_product_review(review_id: str, review: SchemaProduct.ProductReview, db: Session = Depends(get_db)):
    db_review = db.query(ModelProduct.ProductReview).filter(ModelProduct.ProductReview.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Product review not found")
    db_review.name = review.name
    db_review.points = review.points
    db_review.description = review.description
    db_review.advantages = review.advantages
    db_review.disadvantages = review.disadvantages
    db.commit()
    return db_review

@admin_router.delete("/product_reviews/{review_id}")
def delete_product_review(review_id: str, db: Session = Depends(get_db),
                          admin_auth=Depends(admin_auth_middleware)):
    review = db.query(ModelProduct.ProductReview).filter(ModelProduct.ProductReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Product review not found")
    db.delete(review)
    db.commit()
    return {"message": "Product review deleted"}


# Tags
@router.get("/tags/")
def read_tags(db: Session = Depends(get_db)):
    return db.query(ModelProduct.Tag).all()

@router.get("/tags/{tag_id}")
def read_tag(tag_id: str, db: Session = Depends(get_db)):
    tag = db.query(ModelProduct.Tag).filter(ModelProduct.Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@admin_router.post("/create_tag/", response_model=SchemaProduct.Tag, status_code=201)
def create_tag(tag: SchemaProduct.Tag, db: Session = Depends(get_db),
               admin_auth=Depends(admin_auth_middleware)):
    info = tag.model_dump()
    new_tag = ModelProduct.Tag(**info)
    db.add(new_tag)
    db.commit()
    return new_tag

@admin_router.put("/tags/{tag_id}")
def update_tag(tag: SchemaProduct.Tag, tag_id: str, db: Session = Depends(get_db),
               admin_auth=Depends(admin_auth_middleware)):
    db_tag = db.query(ModelProduct.Tag).filter(ModelProduct.Tag.id == tag_id).first()
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    db_tag.name = tag.name
    db.commit()
    return db_tag

@admin_router.delete("/tags/{tag_id}")
def delete_tag(tag_id: str, db: Session = Depends(get_db),
               admin_auth=Depends(admin_auth_middleware)):
    tag = db.query(ModelProduct.Tag).filter(ModelProduct.Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    db.delete(tag)
    db.commit()
    return {"message": "Tag deleted"}




@router.get("/product_tags/")
def read_product_tags(db: Session = Depends(get_db)):
    return db.query(ModelProduct.ProductTag).all()

@router.get("/product_tags/{product_id}")
def read_product_tags_by_product(product_id: str, db: Session = Depends(get_db)):
    product_tags = db.query(ModelProduct.ProductTag).filter(ModelProduct.Tag == product_id).all()
    if not product_tags:
        raise HTTPException(status_code=404, detail="Product tags not found")
    return product_tags

@admin_router.post("/product_tags/")
def create_product_tag(product_tag: SchemaProduct.ProductTag, db: Session = Depends(get_db),
                       admin_auth=Depends(admin_auth_middleware)):
    db.add(product_tag)
    db.commit()
    return product_tag

@admin_router.delete("/product_tags/{product_id}/{tag_id}")
def delete_product_tag(product_id: str, tag_id: str, db: Session = Depends(get_db),
                       admin_auth=Depends(admin_auth_middleware)):
    product_tag = db.query(ModelProduct.ProductTag).filter(ModelProduct.ProductTag.product_id == product_id, ModelProduct.ProductTag.tag_id == tag_id).first()
    if not product_tag:
        raise HTTPException(status_code=404, detail="Product tag not found")
    db.delete(product_tag)
    db.commit()
    return {"message": "Product tag deleted"}


@admin_router.post("/create_image", status_code=201)
def upload_image(image: UploadFile=File(...), product_id:str=Form(...),
                 db: Session=Depends(get_db), admin_auth=Depends(admin_auth_middleware)):
    if db.query(ModelProduct.Product).filter(ModelProduct.Product.id == product_id):
        bucket = BucketObj(file=image.file, save_name=str(product_id),
                           destination="/images/products")
        bucket.upload_image()
        new_image = ModelProduct.Image(id = f"{product_id}-{current_time()}",
                                       product_id=product_id,
                                       url = bucket.perma_link())
        db.add(new_image)
        db.commit()
        return new_image
    raise HTTPException(status_code=404, detail="Product category not found")



@router.get("/list/product-image")
def get_products(limit:int =0, db: Session=Depends(get_db)):
    """ returns products with first related image"""
    products = db.query(ModelProduct.Product).options(joinedload(ModelProduct.Product.image)).limit(limit).all()
    transformed_products = []
    for product in products:
        transformed_product = {
            "price_after_discount": product.price_after_discount,
            "modified_at": product.modified_at,
            "name": product.name,
            "warranty": product.warranty,
            "deleted_at": product.deleted_at,
            "discount_id": product.discount_id,
            "description": product.description,
            "survay": product.survay,
            "category_id": product.category_id,
            "id": product.id,
            "original_price": product.original_price,
            "brand": product.brand,
            "created_at": product.created_at,
            "image": [{"url": image.url} for image in product.image]  # Modify this line
        }
        transformed_products.append(transformed_product)

    return transformed_products

@router.get("/list/product-image-size" ,status_code=200)
def product_n_image_n_size(limit:int =0, db: Session=Depends(get_db)):
    products = db.query(ModelProduct.Product).options(joinedload(ModelProduct.Product.image),
                                                      joinedload(ModelProduct.Product.sizes)).limit(limit).all()

    transformed_products = []
    for product in products:
        transformed_product = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "survay": product.survay,
            "original_price": product.original_price,
            "price_after_discount": product.price_after_discount,
            "warranty": product.warranty,
            "discount_id": product.discount_id,
            "category_id": product.category_id,
            "brand": product.brand,
            "created_at": product.created_at,
            "modified_at": product.modified_at,
            "deleted_at": product.deleted_at,
            "image": [{"url": image.url} for image in product.image],  # Only include the URL
            "sizes": [{"size": size.size, "color": size.color, "quantity": size.quantity} for size in product.sizes]  # Include size details
        }
        transformed_products.append(transformed_product)

    return transformed_products