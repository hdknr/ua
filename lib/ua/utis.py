from django.conf import settings
import pykf


def detect_encoding(text):
    return {
        pykf.UTF8: 'utf-8',
        pykf.SJIS: 'shift-jis',
    }.get(pykf.guess(text), settings.DEFAULT_CHARSET)
