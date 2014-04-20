''' docomo featured phone
'''
from . import BaseAgent, DeviceClass


class Agent(BaseAgent):
    COOKIELESS = True
    CLASS = DeviceClass.PHONE
