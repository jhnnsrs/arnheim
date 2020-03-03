from rest_access_policy import AccessPolicy


class ExternalAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["*"],
            "principal": "authenticated",
            "effect": "allow"
        },
        {
            "action": ["recent"],
            "principal": ["*"],
            "effect": "allow"
        }
    ]