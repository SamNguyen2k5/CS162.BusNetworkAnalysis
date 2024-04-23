"""
Input mixins for the PathQuery class
"""
import ndjson
from elements.path import Path

class PathQueryInputMixin:
    """
    Input mixins for the PathQuery class
    """
    @classmethod
    def from_ndjson(cls, file: str = 'paths.json'):
        """
        Import a list of Paths into a VariantQuery object.
        """
        with open(file, 'r', encoding='utf-8') as f:
            obj = ndjson.load(f)
            return cls({
                (int(path['RouteId']), int(path['RouteVarId'])): Path.from_dict(path) 
                for path in obj
            })