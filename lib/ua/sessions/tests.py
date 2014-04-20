# -*- coding: utf-8 -*-

import os

from django.core.management import call_command
from django.conf.urls import patterns, url   # , include

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect


MODULE, _ = os.path.splitext(os.path.basename(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", MODULE)


# SETTINGS ------------------------
#DEBUG = True
#SECRET_KEY = 'secret'
ROOT_URLCONF = MODULE
INSTALLED_APPS = (
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.auth',
    'django.contrib.admin',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ua.sessions.middleware.UrlBasedSessionMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',
)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

if not settings.configured:
    settings.configure(**locals())


# Views -------------------------
def home(request):
    return HttpResponse('OK')


def agent(request):
#    from utils import session_embedded_url
    print request.get_host()     # dir(request)
    return HttpResponseRedirect(
        '/redir?agent=' + request.agent.CLASS.value)
#        session_embedded_url(request,
#    )


def redir(request):
    session_key = request.session and request.session.session_key
    return HttpResponse(
        session_key + ":" +
        request.META.get('HTTP_USER_AGENT', 'N/A'))


# URLS ---------------------------
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns(
    '',
    url('^redir', redir, name="redir", ),
    url('^agent', agent, name="agent", ),
    url('^$', home, name="home", ),
    #    ('^admin/', include(admin.site.urls)),
)

# TESTS ----------------

from django.test import TestCase, client


class TestUtils(TestCase):
    def setUp(self):
        pass

    def test_featured(self):
        self.client = client.Client(
            HTTP_USER_AGENT="KDDI-HI31 UP.Browser/6.2.0.5 (GUI) MMP/2.0",
        )
        res = self.client.get('/agent', follow=True)
        print res.content
        print res.redirect_chain

    def test_pc(self):
        self.client = client.Client(
            HTTP_USER_AGENT="Mozilla/4.0 (compatible; MSIE 5.01; Windows NT)",
        )
        res = self.client.get('/agent', follow=True)
        print res.content
        print res.redirect_chain

if __name__ == '__main__':
    call_command('test')
