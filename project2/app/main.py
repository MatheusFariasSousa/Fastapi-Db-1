from fastapi import FastAPI
from app.routes.category_routes import router as category_router
from app.routes.product_routes import router as product_routes

app=FastAPI()


@app.get("/index")

def hello_world():
    return "hello world"

app.include_router(category_router)
app.include_router(product_routes)