import re
from urlparse import urlparse

from django.contrib.auth import login as auth_login
from django.core.urlresolvers import reverse as default_reverse

SESSION_EMBEDDED_URL_PATTERN = r'^(?P<path_info>.*);\((?P<session_key>.+)\)'


def from_url(path_info, path=None):
    """ path = script_name + path_info
    """
    m = re.search(SESSION_EMBEDDED_URL_PATTERN, path_info)
    m = m and m.groupdict()
    if m:
        path = path or path_info
        m['path'] = re.sub(SESSION_EMBEDDED_URL_PATTERN, '\g<1>', path)
    return m


def to_url(url, session_key):
    u = urlparse(url)
    val = dict(
        path=u.path,
        query='?' + u.query if u.query else '',
        fragment='#' + u.fragment if u.fragment else '',
        session_key=session_key
    )
    return "{path};({session_key}){query}{fragment}".format(**val)


def is_valid_session(request):
    ''' check validity
    '''
    if request.method == "POST":
        if request.session.get('last_csrf_cookie', '') != \
                request.POST.get('csrfmiddlewaretoken', ''):
            return False

    is_valid = True
    # Some carrier changes phone's address.
    # is_valid = request.session.get('login_address', '') == \
    # request.META.get('REMOTE_ADDR','')

    return is_valid


def session_embedded_url(request, url, session='auto'):
    ''' DoCoMo & EZWeb : Session Embedded URL
    '''
    if request is None or session == 'none' or session is None:
        return url

    if session == 'embed' or (
        hasattr(request, 'agent') and request.agent.COOKIELESS
    ):
        url = to_url(url, request.session.session_key)

    return url


def login(request, user):
    ''' after promoting anonymous to logged in user,
        session keys are changed.
    '''
    auth_login(request, user)        # Default
    request.session['session_embedded'] = True
    request.session['login_address'] = request.META.get('REMOTE_ADDR', '')
    # Some carrier changes IP address dynamically.
    request.session.save()


def reverse(viewname, request=None,
            urlconf=None, args=None, kwargs=None,
            prefix=None, current_app=None,
            session="auto"):

    url = default_reverse(
        viewname, urlconf, args, kwargs, prefix, current_app)
    return session_embedded_url(request, url, session)
