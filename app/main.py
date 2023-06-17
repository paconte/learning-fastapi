from fastapi import FastAPI

from app.api.product import product_router
from app.api.user import user_router

app = FastAPI()
app.include_router(user_router)
app.include_router(product_router)
