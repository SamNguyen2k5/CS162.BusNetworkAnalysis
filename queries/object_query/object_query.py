"""
Module queries.object_query
"""
import ndjson
import pandas as pd
from typing import Callable, Any

class ObjectQuery:
    """
    Generic ObjectQuery class. 
    Supports querying a list of objects with certain criteria.
    """
    _objs: dict
    _ObjectType: object

    def __init__(self, objs: dict, ObjectType: object):
        self._objs = objs
        self._ObjectType = ObjectType

    def __repr__(self):
        return '\n'.join(
            obj.__repr__()
            for obj in self._objs.values()
        )
    
    def __len__(self) -> int:
        return len(self._objs)
    
    def __iter__(self):
        return iter(self._objs.values())
    
    def __getitem__(self, obj_id):
        return self._objs[obj_id]
    
    @property
    def ids(self):
        """
        Returns IDs of items.
        """
        return self._objs.keys()
    
    @property
    def values(self):
        """
        Returns values of items.
        """
        return list(self._objs.values())
    
    def query_to_dict(self, pred: Callable):
        """
        Queries all items satisfying the predicate pred, return as a dictionary.
        """
        return dict(filter(lambda item: pred(item[1]), self._objs.items()))
    
    def search_to_dict(self, attr: str, value: Any) -> dict:
        """
        Searches for all items with attributes matching value, return as a dictionary.
        """
        if not hasattr(self._ObjectType, attr):
            raise AttributeError
        
        return self.query_to_dict(lambda obj: getattr(obj, attr) == value)
    
    def to_pandas(self, **kwargs):
        """
        Exports ObjectQuery information to a pandas DataFrame. 
        """
        return pd.DataFrame((obj.to_dict() for obj in self._objs.values()), **kwargs)

    def to_csv(self, file: str, **kwargs):
        """
        Exports ObjectQuery information to CSV file. 
        The function converts the dictionary _objs into a pandas table before exporting to CSV.
        """
        self.to_pandas().to_csv(file, index=False, **kwargs)

    def to_json(self, file: str):
        """
        Exports ObjectQuery information to JSON file. 
        The function dumps the dictionary _objs into a JSON file.
        """
        json_objs = [obj.to_dict() for obj in self._objs.values()]
        with open(file, 'w', encoding='utf-8') as f:
            ndjson.dump(json_objs, f, ensure_ascii=False)

    def to_dict(self):
        """
        Returns internal state _objs.
        """
        return self._objs
    
    # Aliases
    output_as_json = to_json
    output_as_csv = to_csv