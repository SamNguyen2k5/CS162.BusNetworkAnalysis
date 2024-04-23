"""
Input mixins for the VariantQuery class
"""
import ndjson
from elements.variant import Variant

class VariantQueryInputMixin:
    """
    Input mixins for the VariantQuery class
    """
    @classmethod
    def from_ndjson(cls, file: str = 'vars.json'):
        """
        Import a list of Variants into a VariantQuery object.
        """
        with open(file, 'r', encoding='utf-8') as f:
            obj = ndjson.load(f)
            return cls({
                (int(variant['RouteId']), int(variant['RouteVarId'])): Variant.from_dict(variant) 
                for route in obj
                for variant in route
            })