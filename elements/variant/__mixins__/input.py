"""
Input mixins for the Variant class.
"""
import ndjson

class VariantInputMixin:
    """
    Input mixins for the Variant class.
    """
    @classmethod
    def from_dict(cls, kwargs):
        """
        Create Variant from a Python dictionary.
        """
        return cls(**kwargs)
    
    @classmethod
    def from_json(cls, file):
        """
        Create Variant from JSON file. 
        The function loads a JSON file into a Python dictionary, then call from_dict().
        """
        with open(file, 'r', encoding='utf-8') as f:
            objs = ndjson.load(f)
            return cls(**objs[0])
