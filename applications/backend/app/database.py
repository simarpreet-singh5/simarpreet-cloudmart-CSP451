import os
from typing import List, Dict, Any

from azure.cosmos import CosmosClient, exceptions

COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY")
DATABASE_NAME = "cloudmart"

_use_cosmos = bool(COSMOS_ENDPOINT and COSMOS_KEY)

# Fallback in-memory data for local dev
_fake_products = [
    {
        "id": "1",
        "name": "Wireless Headphones Pro",
        "description": "Premium noise-cancelling wireless headphones with 30hr battery",
        "category": "Electronics",
        "price": 199.99,
        "stock": 50,
    },
    {
        "id": "2",
        "name": "4K Smart TV 55\"",
        "description": "55-inch Ultra HD Smart TV with HDR",
        "category": "Electronics",
        "price": 699.99,
        "stock": 20,
    },
]

_fake_cart: List[Dict[str, Any]] = []
_fake_orders: List[Dict[str, Any]] = []

if _use_cosmos:
    try:
        client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
        db = client.get_database_client(DATABASE_NAME)
        products_container = db.get_container_client("products")
        cart_container = db.get_container_client("cart")
        orders_container = db.get_container_client("orders")
    except Exception:
        _use_cosmos = False
else:
    products_container = cart_container = orders_container = None


def get_products():
    if _use_cosmos:
        return list(products_container.read_all_items())
    return _fake_products


def get_product(product_id: str):
    if _use_cosmos:
        query = "SELECT * FROM c WHERE c.id = @id"
        params = [{"name": "@id", "value": product_id}]
        items = list(products_container.query_items(
            query=query,
            parameters=params,
            enable_cross_partition_query=True
        ))
        if not items:
            raise exceptions.CosmosResourceNotFoundError
        return items[0]
    for p in _fake_products:
        if p["id"] == product_id:
            return p
    raise KeyError("Product not found")


def get_categories():
    products = get_products()
    return sorted({p["category"] for p in products})


def get_cart():
    if _use_cosmos:
        return list(cart_container.read_all_items())
    return _fake_cart


def add_to_cart(item: dict):
    if _use_cosmos:
        cart_container.create_item(item)
    else:
        _fake_cart.append(item)
    return {"status": "added"}


def remove_from_cart(item_id: str):
    if _use_cosmos:
        cart_container.delete_item(item=item_id, partition_key=item_id)
    else:
        global _fake_cart
        _fake_cart = [i for i in _fake_cart if i.get("id") != item_id]
    return {"status": "removed"}


def create_order(order: dict):
    if _use_cosmos:
        orders_container.create_item(order)
    else:
        _fake_orders.append(order)
    return {"status": "order_created"}


def list_orders():
    if _use_cosmos:
        return list(orders_container.read_all_items())
    return _fake_orders
