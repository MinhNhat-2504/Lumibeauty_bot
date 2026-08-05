import uuid
from datetime import datetime
from database.cosmos import get_container

def _c():
    return get_container("orders", "/user_id")

def create_order(user_id: int, product_name: str, quantity: int, customer_name: str, address: str) -> str:
    order_id = str(uuid.uuid4())
    _c().create_item(body={
        "id": order_id,
        "user_id": str(user_id),
        "customer_name": customer_name,
        "product_name": product_name,
        "quantity": quantity,
        "address": address,
        "status": "Đang xử lý",
        "created_at": datetime.now().isoformat()
    })
    return order_id

def get_orders_by_user(user_id: int) -> list:
    items = _c().query_items(
        query="SELECT * FROM c WHERE c.user_id=@uid ORDER BY c.created_at DESC OFFSET 0 LIMIT 10",
        parameters=[{"name": "@uid", "value": str(user_id)}],
        partition_key=str(user_id)
    )
    return list(items)

def get_all_orders() -> list:
    items = _c().query_items(
        query="SELECT * FROM c ORDER BY c.created_at DESC",
        enable_cross_partition_query=True
    )
    return list(items)

def update_order_status(order_id: str, user_id: str, new_status: str):
    try:
        order = _c().read_item(item=order_id, partition_key=user_id)
        order["status"] = new_status
        _c().replace_item(item=order_id, body=order)
        return True
    except Exception:
        return False
