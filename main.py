#! /usr/bin/env /home/unviray/Bureau/local/ES21/.venv/bin/python
from pyfladesk import init_gui

from es21 import create_app


def main():
    app = create_app()
    init_gui(app, window_title='ES21')


if __name__ == '__main__':
    main()
