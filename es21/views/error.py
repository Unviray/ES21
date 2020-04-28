from flask import render_template as render


def page_not_found(e):
    return render('error/404.html'), 404


def server_error(e):
    return render('error/500.html'), 500
