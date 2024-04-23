"""
Input mixins for the Stop class.
"""
import ndjson

class StopInputMixin:
    """
    Input mixins for the Stop class.
    """
    @classmethod
    def from_dict(cls, kwargs):
        """
        Create Stop from a Python dictionary.
        """
        return cls(**kwargs)
    
    @classmethod
    def from_json(cls, file):
        """
        Create Stop from JSON file. 
        The function loads a JSON file into a Python dictionary, then call from_dict().
        """
        with open(file, 'r', encoding='utf-8') as f:
            objs = ndjson.load(f)
            return cls(**objs[0])
