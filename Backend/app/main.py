from fastapi import FastAPI
import routers.auth as auth
from db import Base, engine


app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(auth.router, tags=["Auth"])
