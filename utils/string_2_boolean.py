def str2bool(v):
    try:
        return v.lower() in ("true", "yes", "ok", "1")
    except AttributeError as attribute_error:
        return False

