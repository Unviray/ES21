"""
es21.config
===========

Base Configuration of es21.
"""

from datetime import date

from .translations import active


month_name = active.month_name
month_short2long = active.month_short2long


class MonthBase(object):
    """
    Dynamic class for working month
    """

    MONTH_NAME = (
        'jan',
        'feb',
        'mar',
        'apr',
        'may',
        'jun',
        'jul',
        'aug',
        'sep',
        'oct',
        'nov',
        'dec', )

    FORMAT = '{month} {year}'

    def __init__(self, obj):
        """
        :param obj: A date or str object
        """

        if isinstance(obj, date):
            self.data = obj
        elif isinstance(obj, str):
            month, year = obj.split('_')
            self.data = date(year, month, 1)  # day 1 is ignored

    @property
    def month(self):
        return self.data.month

    @property
    def year(self):
        return self.data.year

    def __str__(self):
        # - 1 because index start with 0
        m = self.MONTH_NAME[self.data.month - 1]
        y = self.data.year

        return self.FORMAT.format(
            short_month=month_name.get(m),
            month=month_short2long.get(m).title(),
            year=y
        )

    def __sub__(self, n):
        """
        Use to jump {n} month behind
        """
        y = self.data.year
        m = self.data.month

        if n > 0:
            self.data = date(
                year=y - 1 if m == 1 else y,  # last year if today is jan
                month=m - 1 if m > 1 else 12,  # avoid month 0
                day=1, )  # day 1 is ignored

            self - (n - 1)  # recursive until {n} reach 0

        return self

    def __add__(self, n):
        """
        Use to jump {n} month forward
        """
        y = self.data.year
        m = self.data.month

        if n > 0:
            self.data = date(
                year=y + 1 if m == 12 else y,  # last year if today is jan
                month=m + 1 if m < 12 else 1,  # avoid month 0
                day=1, )  # day 1 is ignored

            self + (n - 1)  # recursive until {n} reach 0

        return self


class Config(object):
    y = date.today().year
    m = date.today().month

    last_month = MonthBase(date(year=y, month=m, day=1))  # day 1 is ignored

    MONTH = last_month - 1
