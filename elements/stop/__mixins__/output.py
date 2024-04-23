"""
Output mixins for the Stop class.
"""
import json
from typing import Iterable, Any

class StopOutputMixin:
    """
    Output mixins for the Stop class.
    """
    def to_string(self, MAX_LENGTH: int = 50):
        """
        Display information of a Stop in a string format.
        This function is called by __repr__().
        """

        def safe_join(xs: Iterable):
            return ''.join(filter(lambda x: x is not None, xs))

        return '\n'.join([
            safe_join(['[', self._name, ']']).center(MAX_LENGTH, '='),
            '\n'.join(
                inner_line.ljust(MAX_LENGTH - 1, ' ').ljust(MAX_LENGTH, '|')    
                for inner_line in [
                    safe_join(['| StopID:              ', str(self._stop_id)]),
                    safe_join(['| Code:                ', self._code]),
                    safe_join(['| Name:                ', self._name]),
                    safe_join(['| Type:                ', self._stop_type]),
                    safe_join(['| Zone:                ', self._zone]),
                    safe_join(['| Ward:                ', self._ward]),
                    safe_join(['| Address No.:         ', self._address_no]),
                    safe_join(['| Street:              ', self._street]),
                    safe_join(['| Support Disability?: ', 'True' if self._support_disability else 'False']),
                    safe_join(['| Status:              ', self._status]),
                    safe_join(['| Lng:                 ', str(self._longtitude)]),
                    safe_join(['| Lat:                 ', str(self._latitude)]),
                    safe_join(['| Search tokens:       ', ', '.join(self._search)]),
                    safe_join(['| Routes:              ', ' -> '.join(self._routes)])
                ]
            ),
            ''.ljust(MAX_LENGTH, '=')
        ])
    
    def to_dict(self) -> dict[str, Any]:
        """
        Convert Stop to a Python dictionary
        """
        return {
            'StopId':               self._stop_id,
            'Code':                 self._code,
            'Name':                 self._name,               
            'StopType':             self._stop_type,
            'Zone':                 self._zone,      
            'Ward':                 self._ward,                
            'AddressNo':            self._address_no,
            'Street':               self._street,
            'SupportDisability':    'Có' if self._support_disability else 'Không',
            'Status':               self._status,
            'Lng':                  self._longtitude,
            'Lat':                  self._latitude,
            'Search':               ', '.join(self._search),
            'Routes':               ', '.join(self._routes)   
        }
    
    def to_json(self, file: str) -> None:
        """
        Export Stop information to JSON file. 
        The function calls to_dict() to convert Path to a dictionary, then dumps it into a JSON file.
        """
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False)