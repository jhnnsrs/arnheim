from rest_access_policy import AccessPolicy


class ImportingAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["create","update"],
            "principal": ["group:admin","group:researcher"],
            "effect": "allow"
        },
        {
            "action": ["<safe_methods>"],
            "principal": ["*"],
            "effect": "allow"
        }
    ]