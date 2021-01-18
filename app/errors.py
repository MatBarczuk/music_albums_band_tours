from flask import render_template


def page_not_found(e):
    return render_template('errors/404.html')


def forbidden(e):
    return render_template('errors/403.html')


def internal_server_error(e):
    return render_template('errors/500.html')
