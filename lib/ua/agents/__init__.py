import re
from enum import Enum
from importlib import import_module
import traceback
from logging import getLogger
logger = getLogger()


class BaseEnum(Enum):
    @classmethod
    def create(cls, value, default=None):
        try:
            return cls(value)

        except ValueError:
            return default

        except Exception, e:
            raise e

DeviceClassDict = dict(
    FULL='full',
    SMART='smart',
    PHONE='phone',  # featured phone
    OTHER='other'
)

DeviceClass = type('DeviceClass', (BaseEnum, ), DeviceClassDict)

# http://www.openspc2.org/userAgent/

DETECTOR = [
    # Featured Phone
    r'(?P<agent>DoCoMo)',
    r'(?P<agent>SoftBank)',
    r'^(?P<agent>KDDI)',     # if no KDDI, HDML browser.
    r'(?P<agent>Vodafone)',
    r'(?P<agent>Nokia)',
    r'(?P<agent>MOT-)',
    r'(?P<agent>J-PHONE)',
    r'(?P<agent>BlackBerry)',
    r'(?P<agent>Symbian)',
    # Smart Device
    r'\((?P<agent>iPhone);',
    r'\((?P<agent>iPod)[^;]*;',     # iPod, iPod touch...
    r'\((?P<agent>iPad);',
    r'(?P<agent>Android)',
    r'(?P<agent>Windows\sPhone)',
    # Game Console
    r'(?P<agent>Nitro)',             # Nintendo DS
    r'(?P<agent>PlayStation)',
    r'(?P<agent>Wii)',               # Nintendo DS
    # PC
    r'(?P<agent>Trident)',           # Internet Explorer
    r'(?P<agent>Chrome)',
    r'(?P<agent>Firefox)',
    r'(?P<agent>Safari)',
    #    r'(?P<agent>Lunascape)',
    r'(?P<agent>Opera)',
    r'(?P<agent>MSIE)',
    r'(?P<agent>Konqueror)',
    # Bot
    r'(?P<agent>Googlebot)',
    r'(?P<agent>Yahoo)',
    r'(?P<agent>msnbot)',
    r'(?P<agent>Infoseek)',
]


def agent_type(agent_string):
    for d in DETECTOR:
        m = re.search(d, agent_string, flags=re.IGNORECASE)
        m = m and m.groupdict() or {}
        if m:
            return m['agent'].lower().replace('-', '').replace(' ', '')
    return "generic"


def agent_mod(agent_string):
    mod_name = 'ua.agents.%s' % agent_type(agent_string)
    return import_module(mod_name)


class BaseAgent(object):
    CLASS = DeviceClass.FULL
    COOKIELESS = False

    def __init__(self, agent_string, request=None):
        self.agent_string = agent_string
        self.request = request

    @property
    def name(self):
        return self.__class__.__module__.split('.')[-1]

    def encode_response(self, request, response):
        return response

    def encode_response_shift_jis(self, request, response):
        if not response['content-type'].startswith('text/'):
            return response
        response.content = unicode(
            response.content, 'utf8').encode('cp932', 'replace')
        response['content-type'] = 'application/xhtml+xml; charset=Shift_JIS'
        return response


def agent(agent_string=None, request=None):
    try:
        if not agent_string and request:
            env = getattr(request, 'META', {})
            agent_string = env.get('HTTP_USER_AGENT', '')
        mod = agent_mod(agent_string)
        return getattr(mod, 'Agent')(agent_string, request)
    except:
        logger.error(traceback.format_exc())
        return BaseAgent(agent_string, request)
