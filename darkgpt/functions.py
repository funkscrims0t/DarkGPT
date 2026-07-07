Leak_Function = [
    {
        "name": "dehashed-search",
        "description": "Use for OSINT-style queries",
        "parameters": {
            "type": "object",
            "properties": {
                "mail": {"type": "string", "description": "The mail/domain to search"},
                "nickname": {"type": "string", "description": "The nickname to search"},
            },
            "required": ["mail", "nickname"],
        },
    },
]
