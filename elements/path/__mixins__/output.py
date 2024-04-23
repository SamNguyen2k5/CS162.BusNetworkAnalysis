"""
Output mixins for the Path class.
"""
import json

class PathOutputMixin:
    """
    Output mixins for the Path class.
    """

    def to_string(self):
        """
        Display information of a Path in a string format.
        This function is called by __repr__().
        """
        return '\n'.join(
            '({:9.6f}, {:9.6f})'.format(x, y)
            for (x, y) in self._coords
        )

    def to_dict(self):
        """
        Convert Path to a Python dictionary.
        """
        lat, lng = zip(*self._coords)
        return {
            'lat': lat,
            'lng': lng
        }
    
    def to_json(self, file: str):
        """
        Export Path information to JSON file. 
        The function calls to_dict() to convert Path to a dictionary, then dumps it into a JSON file.
        """
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False)