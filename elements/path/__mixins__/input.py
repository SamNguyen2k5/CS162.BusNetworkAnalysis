"""
Input mixins for the Path class.
"""
import ndjson

class PathInputMixin:
    """
    Input mixins for the Path class.
    """

    @classmethod
    def from_dict(cls, kwargs):
        """
        Create Path from a Python dictionary.
        """
        return cls(**kwargs)
    
    @classmethod
    def from_json(cls, file):
        """
        Create Path from JSON file. 
        The function loads a JSON file into a Python dictionary, then call from_dict().
        """
        with open(file, 'r', encoding='utf-8') as f:
            objs = ndjson.load(f)
            return cls(**objs[0])
