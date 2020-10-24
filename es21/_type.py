"""
es21._type
==========

Top of builting types.
"""

def _int(n):
    """
    Like int() but avoid errors.
    """

    try:
        return int(n)
    except ValueError:
        return 0
    except TypeError:
        return 0

def _sum(list_of_number):
    """
    Like sum() but avoid errors.
    """

    return sum([_int(n) for n in list_of_number])
