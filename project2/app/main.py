from fastapi import FastAPI
from app.routes.category_routes import router as category_router
from app.routes.product_routes import router as product_routes
from app.routes.user_routes import router as user_router


app=FastAPI()


@app.get("/index")

def hello_world():
    return "hello world"

app.include_router(category_router)
app.include_router(product_routes)
app.include_router(user_router)