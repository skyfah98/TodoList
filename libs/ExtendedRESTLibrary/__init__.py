from REST import REST
from .extendedkeywords import ExtendedKeywords
from REST.version import __version__
from REST.compat import IS_PYTHON_2, STRING_TYPES
if IS_PYTHON_2:
    from urlparse import parse_qs, urljoin, urlparse
else:
    from urllib.parse import parse_qs, urljoin, urlparse
from requests.packages.urllib3 import disable_warnings

class ExtendedRESTLibrary(REST, ExtendedKeywords):
    """
    This is extended from RESTinstance library for REST API testing.
    """

    def __init__(
        self,
        url=None,
        ssl_verify=False,
        accept="application/json, */*",
        content_type="application/json",
        user_agent="RESTinstance/%s" % (__version__),
        proxies={},
        schema={},
        spec={},
        instances=[],
        timeout=10
    ):
        """
        Default value for timeouts used with GET, POST, PATCH, PUT, DELETE, OPTIONS, HEAD keywords.
        """
        self.request = {
            "method": None,
            "url": None,
            "scheme": "",
            "netloc": "",
            "path": "",
            "query": {},
            "body": None,
            "headers": {
                "Accept": REST._input_string(accept),
                "Content-Type": REST._input_string(content_type),
                "User-Agent": REST._input_string(user_agent),
            },
            "proxies": REST._input_object(proxies),
            "timeout": [None, None],
            "cert": None,
            "sslVerify": REST._input_ssl_verify(ssl_verify),
            "allowRedirects": True,
        }
        if url:
            url = REST._input_string(url)
            if url.endswith("/"):
                url = url[:-1]
            if not url.startswith(("http://", "https://")):
                url = "http://" + url
            url_parts = urlparse(url)
            self.request["scheme"] = url_parts.scheme
            self.request["netloc"] = url_parts.netloc
            self.request["path"] = url_parts.path
        if not self.request["sslVerify"]:
            disable_warnings()
        self.schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": url,
            "description": None,
            "default": True,
            "examples": [],
            "type": "object",
            "properties": {
                "request": {"type": "object", "properties": {}},
                "response": {"type": "object", "properties": {}},
            },
        }
        self.schema.update(self._input_object(schema))
        self.spec = {}
        self.spec.update(self._input_object(spec))
        self.instances = self._input_array(instances)
        self.timeout = timeout
