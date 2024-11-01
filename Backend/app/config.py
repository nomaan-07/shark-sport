from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import Base, engine
import routers.v2
import routers.v2.admin
import routers.v2.auth
import routers.v2.notification
import routers.v2.product
import routers.v2.user
from models import article, tag, product, user, order, notification


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

user.Base.metadata.create_all(bind=engine) 
product.Base.metadata.create_all(bind=engine) 
article.Base.metadata.create_all(bind=engine) 
tag.Base.metadata.create_all(bind=engine) 
order.Base.metadata.create_all(bind=engine) 
notification.Base.metadata.create_all(bind=engine) 


app.include_router(routers.v2.user.token_router, tags=["Token"])
app.include_router(routers.v2.admin.router, tags=["Admin"])
app.include_router(routers.v2.product.router_admin_content, tags=["Admin Content Management"])
app.include_router(routers.v2.user.router_admin_user, tags=["Admin User Management"])
app.include_router(routers.v2.auth.router, tags=["User-Auth"])
app.include_router(routers.v2.user.router, tags=["User"])
app.include_router(routers.v2.product.router_category, tags=["Category"])
app.include_router(routers.v2.product.router_product, tags=["Product"])
app.include_router(routers.v2.product.router_discount, tags=["Discount"])
app.include_router(routers.v2.product.router_tag, tags=["Tag"])
app.include_router(routers.v2.notification.router, tags=["Notification"])