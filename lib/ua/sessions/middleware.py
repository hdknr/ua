# -*- coding: utf-8 -*-
from ua import agents
import utils

from django.utils.importlib import import_module
from django.conf import settings, global_settings
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http.response import HttpResponseRedirect
from django.template import Template

from urlparse import urlparse


import logging
logger = logging.getLogger(__name__)


class UrlBasedSessionMiddleware(SessionMiddleware):
    cache_key_name = 'session_key_%s'

    def get_agent(self, request):
        agent = getattr(request, 'agent',
                        agents.agent(request=request))
        return agent

    def get_cache_key(self, guid):
        return self.cache_key_name % guid

    def process_request(self, request):
        request.agent = self.get_agent(request)

        if all([
            getattr(request, 'user', None),
            getattr(request.user, 'session', None)
        ]):
            #: if other session middleware found "user" and stored "session",
            #: do nothing
            return

        engine = import_module(settings.SESSION_ENGINE)
        params = utils.from_url(request.path_info, request.path)
        session_key = None

        if params:
            #: session key in URL
            session_key = params['session_key']
            request.path_info = params['path_info']  # rewrite
            request.path = params['path']            # rewrite
            request.session = engine.SessionStore(session_key)

        elif request.agent.COOKIELESS:
            #: no session
            request.session = engine.SessionStore()

        request.session.save()  # just in case

        #: CSRF
        request.COOKIES[global_settings.CSRF_COOKIE_NAME] = \
            request.session.get('last_csrf_cookie',
                                request.POST.get('csrfmiddlewaretoken', ''))

        if request.is_secure() and not request.META.get('HTTP_REFERER'):
            #: SOME AGENTS DOESN'T SEND REFERER.
            request.META['HTTP_REFERER'] = 'https://%s/' % request.get_host()

        #: Reset Logged in user
        delattr(request, '_cached_user')
        AuthenticationMiddleware().process_request(request)

    def process_response(self, request, response):

        if hasattr(request, "session"):
            request.session['last_csrf_cookie'] = \
                request.META.get("CSRF_COOKIE", '')

            if isinstance(
                response, HttpResponseRedirect
            ) and request.agent.COOKIELESS:
                purl = urlparse(response.url)
                if not purl.netloc or purl.netloc == request.get_host():
                    response = HttpResponseRedirect(
                        utils.to_url(purl,
                                     request.session.session_key))

        return super(UrlBasedSessionMiddleware,
                     self).process_response(request, response)


class TemplateResolve(object):
    def process_template_response(self, request, response):
        '''  called by views with django.template.response.TemplateResponse
        '''

        if hasattr(response, "template_name"):
            if not isinstance(response.template_name, Template):
                templates = utils.get_templates(request, response)
                response.template_name = templates

        return response
