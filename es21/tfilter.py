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
