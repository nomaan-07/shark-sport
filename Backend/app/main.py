from fastapi import FastAPI
from db import Base, engine
import models
from routers import category, product, user


app = FastAPI()
Base.metadata.create_all(bind=engine)


app.include_router(category.router, tags=["Product Category"])
app.include_router(product.router, tags=["Prodcts"])
app.include_router(user.router, tags=["User"])