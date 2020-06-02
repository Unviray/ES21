"""ES21
====

Electronic S-21
"""

import pun

import webbrowser


DEFAULT = 'run'


@pun.task()
def run():
    """
    Run server
    """

    webbrowser.open("http://127.0.0.1:5000")
    pun.run('flask run -h 0.0.0.0')
