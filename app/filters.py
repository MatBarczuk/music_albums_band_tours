from babel import dates
from flask import g


def date_format(value):
    return dates.format_date(value, locale=g.lang)
