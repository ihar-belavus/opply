def remove_not_documented_endpoints_preprocessing_hook(endpoints):
    result = []
    for endpoint in endpoints:
        path, path_regex, method, callback = endpoint
        cls = getattr(callback, "cls", None)
        if cls and getattr(cls, "documented", False):
            result.append(endpoint)
    return result
