def update_example(result, generator, request, public):
    if result["components"].get("schemas"):
        for schema in result["components"]["schemas"].values():
            for schema_property in schema["properties"].values():
                if schema_property.get("default"):
                    schema_property["example"] = schema_property.pop("default")
    return result