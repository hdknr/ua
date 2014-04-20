from .iphone import Agent as BaseAgent
from ua.agents import DeviceClass


class Agent(BaseAgent):
    CLASS = DeviceClass.SMART
