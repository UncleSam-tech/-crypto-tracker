# api/index.py

def handler(request):
    name = request.get("query", {}).get("name", "World")
    return {
        "statusCode": 200,
        "headers": { "Content-Type": "application/json" },
        "body": f"Hello, {name}!"
    }
