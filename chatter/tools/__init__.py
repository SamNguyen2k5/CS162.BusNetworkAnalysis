"""
module chatter.tools
"""
from typing import Any, Optional, Type

from langchain.pydantic_v1 import BaseModel, Field
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

from langchain.tools import tool
from queries import StopQuery, VariantQuery, PathQuery

def search_stop(attr: str, value: str | int):
    """
    Search for stops with attribute attr containing the given value.
    - stops:    Set of stops to be searched.
    - attr:     Attribute to be queried.
    - value:    Target value for the attribute.
    """
    return stops.search(attr, value)