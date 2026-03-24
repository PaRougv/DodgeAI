ALLOWED = [
    "sales",
    "billing",
    "delivery",
    "invoice",
    "payment",
    "customer",
    "product",
]

def validate(query):

    q = query.lower()

    for word in ALLOWED:
        if word in q:
            return True

    return False