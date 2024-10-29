from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import Base, engine
import routers
import routers.admin
import routers.product
import routers.user
import tools




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify the origins you want to allow
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine) 


app.include_router(routers.admin.router, tags=['Admin-auth'])
app.include_router(routers.user.router, tags=['User'])
app.include_router(routers.user.admin_router, tags=["Admin-User"])
app.include_router(routers.product.router, tags=["Product"])
app.include_router(routers.product.admin_router, tags=["Admin-Product"])
app.include_router(tools.router, tags=["tools"])