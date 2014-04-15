import re
from enum import Enum
from django.utils.importlib import import_module


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
    FULL='pc',
    SMART='sp',
    FEATURED='fp',
    OTHER='ot'
)

DeviceClass = type('DeviceClass', (BaseEnum, ), DeviceClassDict)

# http://www.openspc2.org/userAgent/

DETECTOR = [
    # Mobile and Others
    r'(?P<agent>DoCoMo)',
    r'(?P<agent>SoftBank)',
    r'^(?P<agent>KDDI)',              # if no KDDI, HDML browser.
    r'(?P<agent>Vodafone)',
    r'(?P<agent>Nokia)',
    r'(?P<agent>MOT-)',
    r'(?P<agent>J-PHONE)',
    r'\((?P<agent>iPhone);',
    r'\((?P<agent>iPod);',
    r'\((?P<agent>iPad);',
    r'(?P<agent>Android)',
    r'(?P<agent>Nitro)',             # Nintendo DS
    r'(?P<agent>Wii)',               # Nintendo DS
    r'(?P<agent>PlayStation)',
    r'(?P<agent>Windows\sPhone)',
    r'(?P<agent>BlackBerry)',
    r'(?P<agent>Symbian)',
    # PC
    r'(?P<agent>Trident)',           # Internet Explorer
    r'(?P<agent>Chrome)',
    r'(?P<agent>Firefox)',
    r'(?P<agent>Safari)',
    r'(?P<agent>Lunascape)',
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


def agent(agent_string=None, request=None):
    if not agent_string and request:
        env = getattr(request, 'META', {})
        agent_string = env.get('HTTP_USER_AGENT', '')
    mod = agent_mod(agent_string)
    return getattr(mod, 'Agent')(agent_string, request)


class BaseAgent(object):
    CLASS = DeviceClass.FULL
    COOKIELESS = False

    def __init__(self, agent_string, request=None):
        self.agent_string = agent_string
        self.request = request
