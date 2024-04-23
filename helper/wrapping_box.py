"""
Helper outputing methods.
"""
from typing import Iterable

def wrapping_box(
    title: str, 
    obj: dict,
    MID_LENGTH: int = 30,
    MAX_LENGTH: int = 50
) -> str:
    """
    Returns a string representing a dictionary wrapped in a box.
    Arguments:
        - obj:              The dictionary to be parsed;
        - MID_LENGTH:       Middle dividing column offset;
        - MAX_LENGTH:       Last column offset

    Example:
    ===============[Đền Trần Hưng Đạo]================
    | StopID:              726                       |
    | Code:                Q1 073                    |
    | Name:                Đền Trần Hưng Đạo         |
    | Type:                Trụ dừng                  |
    | Zone:                Quận 1                    |
    | Ward:                                          |
    | Address No.:         18                        |
    | Street:              Võ Thị Sáu                |
    | Support Disability?: False                     |
    | Status:              Đang khai thác            |
    | Lng:                 106.695238                |
    | Lat:                 10.791369                 |
    | Search tokens:       DTHD,, 18,, VTS           |
    | Routes:              10 -> 18 -> 91            |
    ==================================================
    """
    
    def safe_join(xs: Iterable):
        return ''.join(filter(lambda x: x is not None, xs))

    return '\n'.join([
        safe_join(['[', title, ']']).center(MAX_LENGTH, '='),
        '\n'.join(
            safe_join([
                safe_join(['| ', key, ':']).ljust(MID_LENGTH, ' '),
                str(obj[key])
            ]).ljust(MAX_LENGTH - 1, ' ').ljust(MAX_LENGTH, '|')    
            for key in obj
        ),
        ''.ljust(MAX_LENGTH, '=')
    ])