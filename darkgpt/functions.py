Leak_Function = [
    {
        "type": "function",
        "name": "dehashed_search",
        "description": "Use for OSINT-style queries",
        "parameters": {
            "type": "object",
            "properties": {
                "mail": {
                    "type": ["string", "null"],
                    "description": "The mail address or domain to search, if provided.",
                },
                "nickname": {
                    "type": ["string", "null"],
                    "description": "The username to search, if provided.",
                },
            },
            "required": ["mail", "nickname"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]
