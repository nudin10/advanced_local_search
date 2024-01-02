from typing import Callable
from yaml import FullLoader, load
from jsonschema import ValidationError, validate
from src.misc.exceptions import YAMLValidationError

graph_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "nodes": {"type": "array"},
        "w_nodes": {"type": "array"},
    },
    "required": ["name", "nodes", "w_nodes"],
}

solution_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "anyOf": [
            {
                "properties": {
                    "GDA": {
                        "type": "object",
                        "properties": {
                            "paths": {
                                "type": "object",
                                "properties": {
                                    "all": {"type": "array"},
                                    "accepted": {"type": "array"},
                                    "best": {"type": "array"},
                                },
                                "required": ["all", "accepted", "best"],
                            }
                        },
                        "required": ["paths"],
                    },
                }
            },
            {
                "properties": {
                    "HSA": {
                        "type": "object",
                        "properties": {
                            "paths": {
                                "type": "object",
                                "properties": {
                                    "all": {"type": "array"},
                                    "accepted": {"type": "array"},
                                    "best": {"type": "array"},
                                },
                                "required": ["all", "accepted", "best"],
                            }
                        },
                        "required": ["paths"],
                    },
                }
            },
        ],
        "required": ["name"],
    },
}


def validate_schema(schema: str, instance: str):
    try:
        schema = str.lower(schema)
        if schema == "graph":
            validate(load(instance, Loader=FullLoader), graph_schema)
        elif schema == "solution":
            validate(load(instance, Loader=FullLoader), solution_schema)
        else:
            raise ValueError("Invalid schema validation request")
    except ValidationError as e:
        raise YAMLValidationError(f"Schema for {schema} is invalid")
    except Exception:
        raise
