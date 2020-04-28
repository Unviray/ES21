"""
es21.tfilter
============

All template filter goes here.
"""

from .translations import active


def month_name(mn):
    """
    Convert basic month to prettied format
    ex: "feb_2020" -> "february 2020"
    """

    month = mn.split('_')[0]
    year = mn.split('_')[1]

    m = active.month_short2long.get(month, mn.capitalize())

    try:
        return f'{m.capitalize()} {year}'
    except IndexError:
        return mn.capitalize()


def date(d):
    """
    Convert date object to prettie string.
    """

    day = d.day
    month = active.month_list[d.month - 1]
    year = d.year

    return f'{day} {month.title()} {year}'


def pionner_name(pcode):
    """
    Translate database pionner code to pretiie format
    """

    if pcode.istitle():
        pcode = pcode.lower()
    return active.pionner_short2long.get(pcode, pcode)
