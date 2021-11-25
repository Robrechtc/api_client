import requests
import json


class WebClient:

    def __init__(self, api):
        self.api = api

    def GET(self, resource):
        return self._parse_response(requests.get(resource))

    def POST(self, resource, payload, headers):
        pass

    def PUT(self, resource, **kw):
        pass

    def PATCH(self, resource, **kw):
        pass

    def _parse_response(self, response):
        return response.json()
