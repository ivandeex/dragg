from django.utils.timezone import now
from django.utils.formats import localize
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturaltime
from lib.views import get_lang


def timestr(dt):
    # The minus-notation (%-d) removes leading zeros
    if get_lang('en') == 'en':
        return dt.strftime('%b %-d %Y - %I:%M') + dt.strftime('%p').lower()
    return localize(dt)


def timeago(dt, threshold_hours=None):
    delta = now() - dt
    threshold_hours = threshold_hours or settings.AGO_THRESHOLD_HOURS
    if get_lang('en') == 'en' and delta.days == 0 and \
            0 <= delta.total_seconds() / 3600 < threshold_hours:
        return naturaltime(dt)
    return timestr(dt)
