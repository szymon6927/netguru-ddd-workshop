from enum import Enum
from typing import Any, Dict, List, Tuple


def mongo_repo_serializer(data: List[Tuple[str, Any]]) -> Dict[str, Any]:
    result = {}

    for key, value in data:
        if isinstance(value, Enum):
            result[key] = value.value
        elif key == "_domain_events":
            continue
        elif key == "id":
            result["_id"] = value
        else:
            result[key] = value

    return result
