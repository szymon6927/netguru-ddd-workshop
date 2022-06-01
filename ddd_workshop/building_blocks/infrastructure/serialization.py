from enum import Enum
from typing import Any, List, Tuple

from ddd_workshop.building_blocks.custom_types import MongoDocument


def mongo_repo_serializer(data: List[Tuple[str, Any]]) -> MongoDocument:
    result = {}

    for key, value in data:
        if isinstance(value, Enum):
            result[key] = value.value
        elif key == "id":
            result["_id"] = value
        else:
            result[key] = value

    return result
