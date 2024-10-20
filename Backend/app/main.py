from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import Base, engine
import routers.v2
import routers.v2.user
#from routers.v1 import admin, auth, product, user 
"""import routers.v1.admin
import routers.v1.product
import routers.v1.user"""
import routers
import tools


from models import article, tag, product, user, order


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify the origins you want to allow
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

user.Base.metadata.create_all(bind=engine) 
product.Base.metadata.create_all(bind=engine) 
article.Base.metadata.create_all(bind=engine) 
tag.Base.metadata.create_all(bind=engine) 
order.Base.metadata.create_all(bind=engine) 


"""app.include_router(routers.v1.admin.router, tags=['v1-Admin-auth'])
app.include_router(routers.v1.user.router, tags=['v1-User'])
app.include_router(routers.v1.user.admin_router, tags=["v1-Admin-User"])
app.include_router(routers.v1.product.router, tags=["v1-Product"])
app.include_router(routers.v1.product.admin_router, tags=["v1-Admin-Product"])"""
app.include_router(tools.router, tags=["v1-tools"])

"""----------------------------------------------------------- v2 section------------------------------------------------"""

app.include_router(routers.v2.user.router, tags=["Register","SignUp"])