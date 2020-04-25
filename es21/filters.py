"""
es21.filters
============

Include all filters of preachers.
"""

from flask import current_app as app


class Filter(object):
    def __init__(self, preachers):
        self.preachers = preachers
        self.filters = dict()  # list of registered filters
        self.filtered_by = []  # list of executed filters

        self.register_filter(returned)
        self.register_filter(not_returned)

    def __call__(self, filter_name, *args, **kwargs):
        """
        Do filtering
        """

        func = self.filters.get(filter_name)

        if func is not None:
            # func(*args, **kwargs) produce a function
            result = filter(func(*args, **kwargs), self.preachers)
            self.preachers = list(result)

            self.filtered_by.append(filter_name)

    def register_filter(self, filter_func, name=None):
        if name is not None:
            self.filters[name] = filter_func
        else:
            self.filters[filter_func.__name__] = filter_func


def returned(month=None):
    """
    Check if preacher return his report
    :return: a function for filter()
    """

    # TODO: change this to a decorator 'with_month'
    month = month or str(app.config['MONTH'])

    def func(preacher):
        try:
            hour = preacher['tatitra'][month]['ora']
            return hour != 0

        except KeyError:
            return False

    return func


def not_returned(month=None):
    """
    Check if preacher return his report
    :return: a function for filter()
    """

    # TODO: change this to a decorator 'with_month'
    month = month or str(app.config['MONTH'])

    def func(preacher):
        try:
            hour = preacher['tatitra'][month]['ora']
            return hour == 0

        except KeyError:
            return True

    return func
