auth_schema = {
    "type": "object",
    "properties": {
        "login": {
            "type": "string",
            "message": {
                "type": "login должен быть текстом",
            },
        },
        "password": {
            "type": "string",
            "pattern": "^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).+$",
            "message": {
                "type": "Пароль должен быть передан как текст",
                "pattern": "В пароле должна быть хотя бы одна цифра, строчная или большая буква"
            },
        },
    },
    "required": ["login", "password"],
    "message": {
        "type": "Данные должны быть json объектом",
    },
    "additionalProperties": True,
}