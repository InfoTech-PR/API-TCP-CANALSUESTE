def to_serializable(obj):
    if isinstance(obj, dict):
        return {key: to_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [to_serializable(item) for item in obj]
    elif hasattr(obj, '__dict__'):
        return to_serializable(obj.__dict__)
    else:
        return obj