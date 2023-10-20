update_product = {
    "type": "object",
    "properties": {
        "id": {
            "type": "number",
            "message": {
                "type": "id должен быть числом",
            },
        },
        "name": {
            "type": "string",
            "message": {
                "type": "Название продукта должна быть string значеним",
            },
        },
        "price": {
            "type": "number",
            "message": {
                "type": "Цена должна быть передана как число",
            },
        },
    },
    "message": {
        "type": "Данные должны быть json объектом",
    },
    "additionalProperties": False,
}
