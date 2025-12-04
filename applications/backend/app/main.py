from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .database import (
    get_products,
    get_product,
    get_categories,
    get_cart,
    add_to_cart,
    remove_from_cart,
    create_order,
    list_orders
)

app = FastAPI(title="CloudMart API")

# Serve static frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve index.html at root
@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/v1/products")
def products():
    return get_products()


@app.get("/api/v1/products/{product_id}")
def product(product_id: str):
    item = get_product(product_id)
    if not item:
        raise HTTPException(status_code=404, detail="Product not found")
    return item


@app.get("/api/v1/categories")
def categories():
    return get_categories()


@app.get("/api/v1/cart")
def cart():
    return get_cart()


@app.post("/api/v1/cart/items")
def add_item(item: dict):
    return add_to_cart(item)


@app.delete("/api/v1/cart/items/{item_id}")
def delete_item(item_id: str):
    return remove_from_cart(item_id)


@app.post("/api/v1/orders")
def order(order: dict):
    return create_order(order)


@app.get("/api/v1/orders")
def orders():
    return list_orders()
