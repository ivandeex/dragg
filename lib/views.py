from django.utils.translation import get_language


def get_lang(default):
    lang = get_language()
    return lang if lang and lang != 'en-us' else default
