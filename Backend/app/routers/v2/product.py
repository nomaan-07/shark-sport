from fastapi import APIRouter, HTTPException, Request, Form, File, Query,UploadFile, Depends, Response
from db import get_db, Session, joinedload
from typing import Optional, List
from models.product import Product as ProductModel
from models.product import ProductCategory as PCategoryModel
from models.product import ProductImage, FavoritProduct
from models.tag import ProductTag
from models.product import Specification
from models.product import Discount as Disc_Model
from models.product import Size as SizeModel
from tools import BucketObj_2, current_time, extract_items_from_string
from schemas.product import DiscountBase, Discount, CreateProductResponse, ProductBase
from sqlalchemy import or_
from middleware.auth_middleware import auth_middleware
from models.tag import Tag as TagModel



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

router_tag= APIRouter(
    prefix="/api/tag"
)






@router_admin_content.post("/create_product",response_model=CreateProductResponse, status_code=201)
def create_product(images:List[UploadFile]=File(...),
                   name:str=Form(...),
                   description:str=Form(...),
                   survey:str=Form(...),
                   original_price:int=Form(...),
                   warranty:str=Form(...),
                   discount_id:int=Form(...),
                   category_id:int=Form(...),
                   brand:str=Form(...),
                   sizes:str=Form(...),
                   colors:str=Form(...),
                   qtys:str=Form(...),
                   specification_names:str=Form(...),
                   specification_descriptions:str=Form(...),
                   tags:str=Form(...),
                   db:Session=Depends(get_db),auth_dict=Depends(auth_middleware)
                   ):
    if  auth_dict["user_type"] == "user":
        raise HTTPException(status_code=401, detail="Access denide for users")
    db_product = db.query(ProductModel).filter(ProductModel.name == name).first()
    if db_product:
        raise HTTPException(status_code=409, detail=f"product with name {name} already exists")
    discount_rate = db.query(Disc_Model).filter(Disc_Model.id == discount_id).first().discount_rate
    off_price = original_price - (original_price* (discount_rate/100))
    new_product = ProductModel(name=name,
                               description=description,
                               survey=survey,
                               original_price=original_price,
                               price_after_discount=off_price,
                               discount_id=discount_id,
                               warranty=warranty,
                               category_id=category_id,
                               brand=brand,
                               created_at=current_time())
    db.add(new_product)
    db.commit()
    tags = extract_items_from_string(tags,True)
    for tag in tags:
        db_tag = db.query(TagModel).filter(TagModel.id==int(tag)).first()
        if not db_tag:
            raise HTTPException(status_code=400, detail=f"tag {tag} does not exists")
        product_tag = ProductTag(product_id=new_product.id, tag_id=db_tag.id)
        db.add(product_tag)

    image_objs = BucketObj_2(images,[name+str(i) for i in range(len(images))],"images/products")
    image_objs.upload_images()
    images_urls = image_objs.perma_links
    for url in images_urls:
        product_image = ProductImage(image_url=url, product_id=new_product.id)
        db.add(product_image)
    
    sizes = extract_items_from_string(sizes)
    colors = extract_items_from_string(colors)
    qtys = extract_items_from_string(qtys,True)
    added_sizes = []
    for size,color,qty in zip(sizes,colors,qtys):
        product_size = SizeModel(product_id=new_product.id, size=size, color=color,
                                 quantity=int(qty))
        db.add(product_size)
        added_sizes.append({"size":size, "color":color, "quantity":qty})

    specification_names = extract_items_from_string(specification_names)
    specification_descriptions = extract_items_from_string(specification_descriptions)
    store_spec_name_desc = []
    for specifc_name, specific_desc in zip(specification_names, specification_descriptions):
        new_product_specification = Specification(product_id=new_product.id, name=specifc_name, description=specific_desc)
        db.add(new_product_specification)
        store_spec_name_desc.append({specifc_name:specific_desc})

    db.commit()
    return {
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
    "created_at": new_product.created_at,
    "tags": tags,
    "specifications": store_spec_name_desc,
    "sizes": added_sizes,
    "images": images_urls
    }

        


@router_product.get("/products/{product_id}", status_code=200)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router_product.get("/list_products", status_code=200)
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

@router_admin_content.delete("/products/{product_id}", response_model=ProductBase, status_code=200)
def delete_product(product_id: int, db: Session = Depends(get_db), auth_dict=Depends(auth_middleware)):
    if  auth_dict["user_type"] == "user":
        raise HTTPException(status_code=401, detail="Access denide for users")
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    new_notific = NotificationModel(subject=f"حذف کردن محصول", message=f"محصول با این مشخصات حذف شد : {product_id} - {db_product.name}",
                                    admin_id = auth_dict["uid"], created_at = current_time())
    db.add(new_notific)
    db.commit()
    return db_product





"""----------------------------------------Category Section----------------------------"""





from schemas.product import Category,CategoryCreate

@router_admin_content.post("/create_category", response_model=CategoryCreate, status_code=200)
def create_category(image:UploadFile=File(...), name: str=Form(...), description:str=Form(...,max_length=300),
                    db:Session=Depends(get_db), auth_dict = Depends(auth_middleware)):
    if  auth_dict["user_type"] == "user":
        raise HTTPException(status_code=401, detail="Access denide for users")
    if db.query(PCategoryModel).filter(PCategoryModel.name == name).first():
        raise HTTPException(status_code=409, detail=f"Category {name} already exists")
    image_url = BucketObj_2(image, [name], destination="/ProductCategories").perma_links
    new_category = PCategoryModel(image_url=image_url[0], name=name, description=description, created_at=current_time())
    db.add(new_category)
    db.commit()
    new_notific = NotificationModel(subject=f"اضافه کردن دسته بندی محصولات", message=f"{new_category.name} با موفقیت اضافه شد",
                                    admin_id = auth_dict["uid"], created_at = current_time())
    db.add(new_notific)
    db.commit()
    return new_category


@router_category.get("/list/", response_model=List[Category])
def read_categories(index:bool=True,skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    categories = db.query(PCategoryModel)
    if index:
        categories = categories.order_by(PCategoryModel.created_at.desc())
    return categories.offset(skip).limit(limit).all()


@router_category.get("/get/{category_id}", response_model=Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(PCategoryModel).filter(PCategoryModel.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router_category.put("/update/{category_id}", response_model=Category)
def update_category(
    category_id: int,
    image: Optional[UploadFile] = File(None),
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None, max_length=300),
    db: Session = Depends(get_db), auth_dict=Depends(auth_middleware)
    ):
    if  auth_dict["user_type"] == "user":
        raise HTTPException(status_code=401, detail="Access denide for users")
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


@router_category.delete("/delete/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db), auth_dict=Depends(auth_middleware)):
    if  auth_dict["user_type"] == "user":
        raise HTTPException(status_code=401, detail="Access denide for users")
    db_category = db.query(PCategoryModel).filter(PCategoryModel.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return db_category



"""----------------------------------------discount Section----------------------------"""






@router_admin_content.post("/discount/create_discount", response_model=Discount, status_code=201)
def create_discount(discount: DiscountBase, db: Session = Depends(get_db), auth_dict=Depends(auth_middleware)):
    if  auth_dict["user_type"] == "user":
        raise HTTPException(status_code=401, detail="Access denide for users")
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
    new_notific = NotificationModel(subject=f"اضافه کردن کد تخفیف", message=f"{discount.discount_code} با موفقیت اضافه شد",
                                    admin_id = auth_dict["uid"], created_at = current_time())
    db.add(new_notific)
    db.commit()
    return db_discount


@router_discount.get("/list_discounts", response_model=list[Discount], status_code=200)
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
    return discounts


@router_discount.get("/read_discount", response_model=Discount, status_code=200)
def read_discount(discount_id: int, db:Session=Depends(get_db)):
    db_discount = db.query(Disc_Model).filter(Disc_Model.id == discount_id).first()
    if not db_discount:
        raise HTTPException(status_code=204, detail="discount not found")
    return db_discount




"""----------------------------------------tag Section----------------------------"""
from schemas.product import TagBase,Tag
from models.notification import Notification as NotificationModel 
@router_admin_content.post("/tag/create", response_model=Tag, status_code=201)
def create_tag(tag: TagBase, db:Session=Depends(get_db), auth_dict=Depends(auth_middleware)):
    if  auth_dict["user_type"] == "user":
        raise HTTPException(status_code=401, detail="Access denide for users")
    db_tag = db.query(TagModel).filter(TagModel.name == tag.name).first()
    if db_tag:
        raise HTTPException(status_code=409, detail=f"Duplicated Tag with name {tag.name}")
    new_tag = TagModel(**tag.model_dump())
    db.add(new_tag)
    db.commit()
    new_notific = NotificationModel(subject=f"اضافه کردن تگ", message=f"{new_tag} با موفقیت اضافه شد",
                                    admin_id = auth_dict["uid"], created_at = current_time())
    db.add(new_notific)
    db.commit()
    return new_tag

@router_tag.get("/get/{tag_id}")
def read_tag(tag_id:int, db:Session=Depends(get_db)):
    db_tag = db.query(TagModel).filter(TagModel.id == tag_id).first()
    if not db_tag:
        raise HTTPException(status_code=204, detail=f"tag with ID {tag_id} not found")
    return db_tag

@router_tag.get("/list_tags")
def list_tags(limit: int=0, skip: int =0, db:Session=Depends(get_db)):
    db_tags = db.query(TagModel).offset(skip).limit(limit).all()
    if not db_tags:
        raise HTTPException(status_code=204, detail=f"There are no tags")
    return db_tags

"""----------------------------------------Address Section----------------------------"""
