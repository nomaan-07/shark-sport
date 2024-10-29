from fastapi import APIRouter, HTTPException, Request, Form, File, Query,UploadFile, Depends, Response
from db import get_db, Session, joinedload
from typing import Optional, List
from models.product import Product as ProductModel
from models.product import ProductCategory as PCategoryModel
from models.product import ProductImage, FavoritProduct
from models.tag import ProductTag
from models.product import Specification
from models.product import Discount as Disc_Model
from models.product import Size
from schemas.product import  Product
from tools import BucketObj_2, current_time
from schemas.product import DiscountBase, Discount
from sqlalchemy import or_
from middleware.auth_middleware import auth_middleware
from models.tag import Tag



router_admin_content = APIRouter (
    prefix="/api/admin/content"
)
router_product= APIRouter(
    prefix="/api/product"
)

router_discount= APIRouter(
    prefix="/api/discount"
)

router_category= APIRouter(
    prefix="/api/category"
)


from schemas.product import CreateProductResponse
@router_admin_content.post("/create_product", response_model=CreateProductResponse,status_code=201)
def create_product(
    images: List[UploadFile] = File(...),
    name: str = Form(...),
    description: str = Form(None),
    survey: str = Form(None),
    original_price: int = Form(...),
    warranty: str = Form(None),
    discount_id: int = Form(...),
    category_id: int = Form(None),
    brand: str = Form(None),
    tags: List[str] = Form(...),
    specification_name: List[str] = Form(...),
    specification_description: List[str] = Form(...),
    size: List[str] = Form(...),
    quantity: List[int] = Form(...),
    color: List[str] = Form(...),
    db: Session = Depends(get_db),
    auth_dict= Depends(auth_middleware)
):
    if db.query(ProductModel).filter(ProductModel.name == name).first():
        raise HTTPException(status_code=409, detail="Duplicated Name for product in db")
    
    if not db.query(PCategoryModel).filter(PCategoryModel.id == category_id).first():
        raise HTTPException(status_code=404, detail="category id is invalid")
    
    discount_db = db.query(Disc_Model).filter(Disc_Model.id == discount_id).first()
    if not discount_db:
        raise HTTPException(status_code=404, detail="Discount id is invalid")
    
    price_after_discount = original_price * (1 - (discount_db.discount_rate / 100))
    
    new_product = ProductModel(
        name=name,
        description=description,
        survey=survey,
        original_price=original_price,
        price_after_discount=price_after_discount,
        warranty=warranty,
        discount_id=discount_id,
        category_id=category_id,
        brand=brand,
        created_at=current_time()
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    for tag_name in tags:
        db_tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not db_tag:
            db_tag = Tag(name=tag_name)
            db.add(db_tag)
            db.commit()
            db.refresh(db_tag)
        new_product_tag = ProductTag(product_id=new_product.id, tag_id=db_tag.id)
        db.add(new_product_tag)

    for name, description in zip(specification_name, specification_description):
        db_spec = Specification(
            name=name,
            description=description,
            product_id=new_product.id
        )
        db.add(db_spec)

    for s, q, c in zip(size, quantity, color):
        db_size = Size(
            size=s,
            color=c,
            quantity=q,
            product_id=new_product.id
        )
        db.add(db_size)
    
    images_urls = BucketObj_2(images, [f"{name}_{i}.jpg" for i in range(len(images))], "/products").perma_links
    for url in images_urls:
        new_product_image = ProductImage(image_url=url, product_id=new_product.id)
        db.add(new_product_image)
    
    db.commit()
    db.refresh(new_product)
    
    return {
        "product": {
            "id": new_product.id,
            "name": new_product.name,
            "description": new_product.description,
            "survey": new_product.survey,
            "original_price": new_product.original_price,
            "price_after_discount": new_product.price_after_discount,
            "warranty": new_product.warranty,
            "discount_id": new_product.discount_id,
            "category_id": new_product.category_id,
            "brand": new_product.brand,
            "created_at": new_product.created_at
        },
        "tags": tags,
        "specifications": [{"name": n, "description": d} for n, d in zip(specification_name, specification_description)],
        "sizes": [{"size": s, "color": c, "quantity": q} for s, c, q in zip(size, color, quantity)],
        "images": images_urls
    }


@router_product.get("/products/")
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = db.query(ProductModel).offset(skip).limit(limit).all()
    return products


@router_product.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router_product.get("/products", status_code=200)
def filter_and_read_products_with_related(
    show_sizes: bool = Query(True),
    show_specifications: bool = Query(True),
    show_tags: bool = Query(True),
    show_deleted: bool = Query(False),
    limit: int = Query(10),
    skip: int = Query(0),
    desc: bool = Query(True),
    db: Session = Depends(get_db)
    ):
    query = db.query(ProductModel)
    
    if not show_deleted:
        query = query.filter(ProductModel.deleted_at == None)
    
    if desc:
        query = query.order_by(ProductModel.created_at.desc())
    else:
        query = query.order_by(ProductModel.created_at.asc())
    
    products = query.offset(skip).limit(limit).all()
    
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    
    response = []
    for product in products:
        product_data = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "survey": product.survey,
            "original_price": product.original_price,
            "price_after_discount": product.price_after_discount,
            "warranty": product.warranty,
            "discount_id": product.discount_id,
            "category_id": product.category_id,
            "brand": product.brand,
            "created_at": product.created_at,
            "deleted_at": product.deleted_at,
            "images": [image.image_url for image in product.images]
        }

        if show_tags:
            product_data["tags"] = [tag.tag.name for tag in product.tags]

        if show_specifications:
            product_data["specifications"] = [{"name": spec.name, "description": spec.description} for spec in product.specifications]
        
        if show_sizes:
            product_data["sizes"] = [{"size": s.size, "color": s.color, "quantity": s.quantity} for s in product.sizes]
        
        response.append(product_data)
    
    return response



"""@router_product.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product"""

@router_admin_content.delete("/products/{product_id}", response_model=Product, status_code=200)
def delete_product(product_id: int, db: Session = Depends(get_db), auth_dict=Depends(auth_middleware)):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return db_product





"""----------------------------------------Category Section----------------------------"""





from schemas.product import Category,CategoryBase,CategoryCreate,CategoryUpdate,ProductCreate

@router_category.post("/create_category", response_model=CategoryCreate, status_code=200)
def create_category(image:UploadFile=File(...), name: str=Form(...), description:str=Form(...,max_length=300),
                    db:Session=Depends(get_db)):
    if db.query(PCategoryModel).filter(PCategoryModel.name == name).first():
        raise HTTPException(status_code=409, detail=f"Category {name} already exists")
    image_url = BucketObj_2(image, [name], destination="/ProductCategories").perma_links
    new_category = PCategoryModel(image_url=image_url[0], name=name, description=description, created_at=current_time())
    db.add(new_category)
    db.commit()
    return new_category


@router_category.get("/categories/", response_model=List[Category])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    categories = db.query(PCategoryModel).offset(skip).limit(limit).all()
    return categories


@router_category.get("/categories/{category_id}", response_model=Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(PCategoryModel).filter(PCategoryModel.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router_category.put("/categories/{category_id}", response_model=Category)
def update_category(
    category_id: int,
    image: Optional[UploadFile] = File(None),
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None, max_length=300),
    db: Session = Depends(get_db)
    ):
    db_category = db.query(PCategoryModel).filter(PCategoryModel.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    if image:
        image_url = BucketObj_2(image, [name or db_category.name], destination="/ProductCategories").perma_links
        db_category.image_url = image_url
    if name:
        db_category.name = name
    if description:
        db_category.description = description
    db_category.modified_at = current_time()
    db.commit()
    db.refresh(db_category)
    
    return db_category


@router_category.delete("/categories/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(PCategoryModel).filter(PCategoryModel.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return None



"""----------------------------------------discount Section----------------------------"""






@router_discount.post("/create_discount", response_model=Discount, status_code=201)
def create_discount(discount: DiscountBase, db: Session = Depends(get_db)):
    db_discount = Disc_Model(
        name=discount.name,
        discount_code=discount.discount_code,
        discount_rate=discount.discount_rate,
        created_at=current_time(),
        expires_at=discount.expires_at
    )
    db.add(db_discount)
    db.commit()
    db.refresh(db_discount)
    return db_discount


@router_discount.get("/list_discounts", response_model=list, status_code=200)
def list_discounts(
    limit: Optional[int] = 10, 
    skip: Optional[int] = 0, 
    expired: Optional[bool] = False, 
    index: Optional[bool] = True,
    db: Session = Depends(get_db)
    ):
    query = db.query(Disc_Model)
    if expired:
        query = query.filter(Disc_Model.expires_at <= current_time())
    else:
        query = query.filter(or_(Disc_Model.expires_at > current_time(), Disc_Model.expires_at == None))
    if index:
        query = query.order_by(Disc_Model.created_at.desc())
    discounts = query.offset(skip).limit(limit).all()
    if not discounts:
        raise HTTPException(status_code=404, detail="No discounts found")    
    return discounts


@router_discount.get("/get_discount/{discount_id}", response_model=Discount, status_code=200)
def read_discount(discount_id: int, db:Session=Depends(get_db)):
    db_discount = db.query(Disc_Model).filter(Disc_Model.id == discount_id).first()
    if not db_discount:
        raise HTTPException(status_code="404", detail="discount not found")
    return db_discount




"""----------------------------------------discount Section----------------------------"""
