def get_lang(request):
    return '' if request.LANGUAGE_CODE == 'en-us' else request.LANGUAGE_CODE
