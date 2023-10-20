from flask import Blueprint, request, g
from .product_service import ProductService
from src.lib.auth import is_auth
from .schemas.create_product_schema import create_product
from .schemas.update_product_schema import update_product
from src.lib.validator import validate_schema
from src.lib.vars.global_prefix import global_prefix
import re

product_service = ProductService()
product = Blueprint("product", __name__, url_prefix=f"{global_prefix}/product")


@product.route("/", methods=["GET"])
def get_all_products():
    args = request.args
    page = 1
    limit = 10
    filter = {}
    if request.args.get("page") is not None:
        page = int(args.get("page"))
    if request.args.get("limit") is not None:
        limit = int(args.get("limit"))
    if (
        request.args.get("filter") is not None
        and re.match(
            r"([a-zA-Z]{1,}):(equal|like|not):([a-zA-Z0-9]{1,})",
            request.args.get("filter"),
        )
        is not None
    ):
        filterSplit = request.args.get("filter").split(":")
        filter = {
            "value": filterSplit[2],
            "field": filterSplit[0],
            "op": filterSplit[1],
        }

    return product_service.get_all_products(
        page=page, limit=limit, sort=[], filter=filter
    )


@product.route("/create", methods=["POST"])
@is_auth()
@validate_schema(create_product)
def create_product():
    data = request.get_json()
    return product_service.create_product(data, g.user["id"])


@product.route("/<int:id>", methods=["GET"])
def get_product(id):
    return product_service.get_product(id)


@product.route("/update", methods=["POST"])
@validate_schema(update_product)
@is_auth()
def update_product():
    data = request.get_json()
    return product_service.update_product(data["id"], data, g.user["id"])


@product.route("/delete", methods=["POST"])
@is_auth()
def delete_product():
    data = request.get_json()
    return product_service.delete_product(data["id"], g.user["id"])


@product.route("/history", methods=["GET"])
def get_history():
    args = request.args
    page = 1
    limit = 10

    if request.args.get("page") is not None:
        page = int(args.get("page"))
    if request.args.get("limit") is not None:
        limit = int(args.get("limit"))

    return product_service.get_history_edit(page, limit)
