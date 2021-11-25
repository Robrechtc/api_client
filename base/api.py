from web_client import WebClient
from endpoint import Endpoint


class API:
    def __init__(self, name, base_url, version, **kw):
        self.name = name
        self.base_url = base_url
        self.version = version
        if kw.get('doc_file', False):
            self._doc_file = kw['doc_file']
        self.get_endpoints()
        self.client = WebClient(api=self)
    
    @property
    def doc_file(self):
        return self._doc_file or "openapi.json"

    @doc_file.setter
    def doc_file(self, new_doc_file):
        if new_doc_file:
            self._doc_file = new_doc_file

    def get_endpoints(self):
        endpoints = self.client.GET(self._get_url(res_name=self.doc_file))
        for endpoint in endpoints:
            self._add_endpoint(endpoint)
            
    def _add_endpoint(self, endpoint):
        if not self.endpoints:
            self.endpoints = []
        self.endpoints.append(Endpoint(endpoint))

    def _get_url(self, res_name='', res_id=0, **kw):
        """
        Combines the base url, version and optional resource name, id and
        eventual keyword args into a URL. This should probably be in utils
        """
        def _append_to_url(base, parameter):
            """
            Parses a parameter, appends it to the base and returns the result
            """
            if isinstance(parameter, int):
                return _append_to_url(base, str(parameter))
            if isinstance(parameter, str):
                if base[-1] != "/":
                    base += "/"
                if parameter[-1] != "/":
                    parameter += "/"
                return base + parameter
            if isinstance(parameter, dict):
                if "?" in base:
                    base, query = base.split("?")
                    query += "&".join(["{key}={value}".format(key=k, value=v)
                        for k, v in parameter.items()])
                else:
                    query = ""
                    for k, v in parameter.items():
                        if not query:
                            query = "?{key}={value}".format(key=k, value=v)
                            continue
                        query += "&{key}={value}".format(key=k, value=v)
                return base + query
        url = _append_to_url(self.base_url, self.version)
        if res_name:
            url += _append_to_url(res_name)
        if self.res_id:
            url += _append_to_url(res_id)
        if kw:
            url += _append_to_url(kw)
        return url
