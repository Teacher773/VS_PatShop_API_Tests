STORE_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "petId": {
            "type": "integer"
        },
        "quantity": {
            "type": "integer"
        },
        "shipDate": {
            "type": "string",
            "format": "date-time",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}\\.\\d{3}Z$"
        },
        "status": {
            "type": "string",
            "enum": ["approved", "unapproved", "placed"]
        },
        "complete": {
            "type": "boolean"
        },
    },
    "required": [
        "id",
        "petId",
        "quantity",
        "status",
        "complete"
    ],
    "additionalProperties": False
}
