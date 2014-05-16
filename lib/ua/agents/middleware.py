# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)


class ResponseEncodingMiddleware(object):
    def process_response(self, request, response):
        agent = getattr(request, 'agent', None)
        return agent and agent.encode_response(
            request, response) or response
