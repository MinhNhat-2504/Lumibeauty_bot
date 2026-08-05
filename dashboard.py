"""
Lumi Beauty – Admin Dashboard
Flask web server phục vụ giao diện quản trị và REST API.
Chạy: python dashboard.py  →  http://localhost:5050
"""

import os
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv

load_dotenv()

from database import users, orders, products

app = Flask(__name__)


# ── Trang chính ──────────────────────────────────────────
@app.route("/")
def index():
    return render_template("dashboard.html")


# ── API: Thống kê ────────────────────────────────────────
@app.route("/api/stats")
def api_stats():
    all_users = users.get_all_users()
    all_orders = orders.get_all_orders()
    all_products = products.get_all_products()

    total_revenue = 0
    for o in all_orders:
        if o.get("status") != "Đã hủy":
            # Tìm giá sản phẩm
            prod = products.get_product_by_name(o.get("product_name", ""))
            price = prod["price"] if prod else 0
            total_revenue += price * o.get("quantity", 1)

    return jsonify({
        "users": len(all_users),
        "orders": len(all_orders),
        "products": len(all_products),
        "revenue": total_revenue,
    })


# ── API: Users ───────────────────────────────────────────
@app.route("/api/users")
def api_users():
    all_users = users.get_all_users()
    search = request.args.get("search", "").lower()
    if search:
        all_users = [
            u for u in all_users
            if search in (u.get("username") or "").lower()
            or search in (u.get("telegram_id") or "").lower()
        ]
    # Chỉ trả về các trường cần thiết
    clean = []
    for u in all_users:
        clean.append({
            "id": u.get("id"),
            "telegram_id": u.get("telegram_id"),
            "username": u.get("username", "unknown"),
            "skintype": u.get("skintype"),
        })
    return jsonify(clean)


@app.route("/api/users/<telegram_id>", methods=["DELETE"])
def api_delete_user(telegram_id):
    ok = users.delete_user(int(telegram_id))
    return jsonify({"success": ok})


# ── API: Orders ──────────────────────────────────────────
@app.route("/api/orders")
def api_orders():
    all_orders = orders.get_all_orders()
    status_filter = request.args.get("status", "")
    if status_filter:
        all_orders = [o for o in all_orders if o.get("status") == status_filter]

    clean = []
    for o in all_orders:
        clean.append({
            "id": o.get("id"),
            "user_id": o.get("user_id"),
            "customer_name": o.get("customer_name"),
            "product_name": o.get("product_name"),
            "quantity": o.get("quantity"),
            "address": o.get("address"),
            "status": o.get("status"),
            "created_at": o.get("created_at"),
        })
    return jsonify(clean)


@app.route("/api/orders/<order_id>", methods=["PATCH"])
def api_update_order(order_id):
    data = request.get_json()
    new_status = data.get("status")
    user_id = data.get("user_id")
    if not new_status or not user_id:
        return jsonify({"success": False, "error": "Missing status or user_id"}), 400
    ok = orders.update_order_status(order_id, user_id, new_status)
    return jsonify({"success": ok})


# ── API: Products ────────────────────────────────────────
@app.route("/api/products")
def api_products():
    all_products = products.get_all_products()
    search = request.args.get("search", "").lower()
    if search:
        all_products = [
            p for p in all_products
            if search in (p.get("name") or "").lower()
            or search in (p.get("description") or "").lower()
        ]

    clean = []
    for p in all_products:
        clean.append({
            "id": p.get("id"),
            "name": p.get("name"),
            "price": p.get("price"),
            "description": p.get("description"),
            "skintype": p.get("skintype", []),
            "image": p.get("image"),
        })
    return jsonify(clean)


# ── Main ─────────────────────────────────────────────────
if __name__ == "__main__":
    print("[Lumi Beauty] Admin Dashboard -> http://localhost:5050")
    app.run(host="0.0.0.0", port=5050, debug=True)
