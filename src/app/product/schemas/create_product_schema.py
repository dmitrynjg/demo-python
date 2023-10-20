from .update_product_schema import update_product

create_product = {**update_product}
create_product['requered'] = ["name", "price"],