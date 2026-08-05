from database.cosmos import get_container

def _c():
    return get_container("products", "/id")

def get_all_products() -> list:
    return list(_c().read_all_items())

def get_products_by_skintype(skintype: str) -> list:
    items = _c().query_items(
        query="SELECT * FROM c WHERE ARRAY_CONTAINS(c.skintype, @s)",
        parameters=[{"name": "@s", "value": skintype}],
        enable_cross_partition_query=True
    )
    return list(items)

def search_products(keyword: str) -> list:
    kw = keyword.lower()
    items = _c().query_items(
        query="SELECT * FROM c WHERE CONTAINS(LOWER(c.name),@k) OR CONTAINS(LOWER(c.description),@k)",
        parameters=[{"name": "@k", "value": kw}],
        enable_cross_partition_query=True
    )
    return list(items)

def get_product_by_name(name: str) -> dict | None:
    items = list(_c().query_items(
        query="SELECT * FROM c WHERE c.name = @n",
        parameters=[{"name": "@n", "value": name}],
        enable_cross_partition_query=True
    ))
    return items[0] if items else None
