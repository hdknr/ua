''' DoCoMo featured phone
'''
from . import BaseAgent, DeviceClass


class Agent(BaseAgent):
    COOKIELESS = True
    CLASS = DeviceClass.PHONE

    def encode_response(self, request, response):
        return self.encode_response_shift_jis(
            request, response)
