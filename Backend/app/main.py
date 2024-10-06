from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import Base, engine
import routers
import routers.product


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify the origins you want to allow
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


app.include_router(routers.product.router, tags=["Products"])
