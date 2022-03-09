"""Add all libraries"""
import base64
from copy import deepcopy
from robot.api.deco import keyword
from robot.api import logger
from REST.keywords import Keywords
from REST.compat import STRING_TYPES
from JSONLibrary import JSONLibrary
from Utilities.dict_management import get_dict_diffs
from Utilities.utilities import print_friendly_message


class ExtendedKeywords(Keywords):
    """This class is extended from Keywords"""
    def __init__(self):
        self.timeout = None

    @keyword
    def get_response_body(self):
        """Returns content of response body"""
        self._last_instance_or_error()
        matches = self._find_by_field("response body", return_schema=False)
        if len(matches) > 1:
            json = [found["reality"] for found in matches]
        else:
            json = matches[0]["reality"]
        return json

    @keyword
    def set_rest_headers(self, headers):
        """
        Alias of set_header keyword.

        *Sets new request headers or updates the existing.*

        Argument:

        ``headers``: The headers to add or update as a JSON object or a
        dictionary.

        Examples:

        | `Set REST Headers` | { "authorization": "Basic QWxhZGRpbjpPcGVuU2VzYW1"} |
        | `Set REST Headers` | { "Accept-Encoding": "identity"} |
        | `Set REST Headers` | ${auth_dict} |
        """
        Keywords.set_headers(self, headers)

    @keyword
    def set_credentials_for_rest(self, username, password):
        """
        Use username and password to add header for basic authentication.
        """
        encode_string = base64.b64encode(str(username + ':' + password).encode())
        self.set_headers({"Authorization": "Basic " + str(encode_string.decode('utf-8'))})

    @keyword
    def clear_headers(self):
        """Clear all existing headers"""
        self.request["headers"] = {}
        return self.request["headers"]

    @keyword
    def get_value_from_rest(self, what="", file_path=None, append=False, sort_keys=False):
        """The copy of the `Output` keyword but is not printed to terminal."""
        if isinstance(what, (STRING_TYPES)):
            if what == "":
                try:
                    json = deepcopy(self._last_instance_or_error())
                    json.pop("schema")
                    json.pop("spec")
                except IndexError:
                    raise RuntimeError(no_instances_error)
            elif what.startswith("schema"):
                logger.warn(
                    "schema is not supported."
                )
                what = what.lstrip("schema").lstrip()
                return self.output_schema(what, file_path, append, sort_keys)
            elif what.startswith(("request", "response", "$")):
                self._last_instance_or_error()
                matches = self._find_by_field(what, return_schema=False)
                if len(matches) > 1:
                    json = [found["reality"] for found in matches]
                else:
                    json = matches[0]["reality"]
            else:
                try:
                    json = self._input_json_as_string(what)
                except ValueError:
                    json = self._input_string(what)
        else:
            json = self._input_json_from_non_string(what)
        sort_keys = self._input_boolean(sort_keys)
        if file_path:
            content = dumps(
                json,
                ensure_ascii=False,
                indent=4,
                separators=(",", ": "),
                sort_keys=sort_keys,
            )
            write_mode = "a" if self._input_boolean(append) else "w"
            try:
                with open(
                        path.join(getcwd(), file_path), write_mode, encoding="utf-8"
                ) as file:
                    if IS_PYTHON_2:
                        content = unicode(content)
                    file.write(content)
            except IOError as ex:
                raise RuntimeError(
                    "Error outputting to file '%s':\n%s" % (file_path, ex)
                )
        return json

    @keyword
    def get_value_from_response_body_by_json_path(self, json_path):
        """Gets value from REST response body using JSONPath
        
        Arguments:
            - ``json_path``: jsonpath expression
        
        Return array of values
        """
        response_body = self.get_response_body()
        obj = JSONLibrary()
        value = obj.get_value_from_json(response_body, json_path)
        return value

    @keyword
    def delete_object_from_response_body_by_json_path(self, json_path):
        """Deletes value from REST response body using JSONPath
        
        Arguments:
            - ``json_path``: jsonpath expression
            
        Return new json object
        
        """
        response_body = self.get_response_body()
        obj = JSONLibrary()
        json_object = obj.delete_object_from_json(response_body, json_path)
        return json_object

    @keyword
    def add_object_to_response_body_by_json_path(self, json_path, object_to_add):
        """Adds a dictionary or list object to REST response body using JSONPath
        
        Arguments:

        - ``json_path`` jsonpath expression
        - ``object_to_add`` dictionary or list object to add
            
        Return new json object
        
        """
        response_body = self.get_response_body()
        obj = JSONLibrary()
        json_object = obj.add_object_to_json(response_body, json_path, object_to_add)
        return json_object

    @keyword
    def update_object_to_response_body_by_json_path(self, json_path, new_value):
        """Updates value to REST response body using JSONPath
        
        Arguments:
        - ``json_path`` jsonpath expression
        - ``new_value`` value to update
            
        Return new json object
        
        """
        response_body = self.get_response_body()
        obj = JSONLibrary()
        json_object = obj.update_value_to_json(response_body, json_path, new_value)
        return json_object

    @keyword
    def head(self, endpoint, timeout=None, allow_redirects=None, validate=True, headers=None):
        """*Sends a HEAD request to the endpoint.*

        The endpoint is joined with the URL given on library init (if any).
        If endpoint starts with ``http://`` or ``https://``, it is assumed
        an URL outside the tested API (which may affect logging).

        *Options*

        ``timeout``: A number of seconds to wait for the response before failing the keyword. If it is not given,
        the default timeout is used instead with the timeout argument when importing the library.

        ``allow_redirects``: If true, follow all redirects.
        In contrary to other methods, no HEAD redirects are followed by default.

        ``validate``: If false, skips any request and response validations set
        by expectation keywords and a spec given on library init.

        ``headers``: The headers to add or override for this request.

        *Examples*

        | `HEAD` | /users/1 |
        | `HEAD` | /users/1 | timeout=0.5 |
        """
        if timeout is None:
            connect_timeout = self.timeout
        else:
            connect_timeout = timeout
        Keywords.head(self, endpoint, connect_timeout, allow_redirects, validate, headers)

    @keyword
    def options(self, endpoint, timeout=None, allow_redirects=None, validate=True, headers=None):
        """*Sends an OPTIONS request to the endpoint.*

        The endpoint is joined with the URL given on library init (if any).
        If endpoint starts with ``http://`` or ``https://``, it is assumed
        an URL outside the tested API (which may affect logging).

        *Options*

        ``timeout``: A number of seconds to wait for the response before failing the keyword. If it is not given,
        the default timeout is used instead with the timeout argument when importing the library.

        ``allow_redirects``: If false, do not follow any redirects.

        ``validate``: If false, skips any request and response validations set
        by expectation keywords and a spec given on library init.

        ``headers``: Headers as a JSON object to add or override for the request.

        *Examples*

        | `OPTIONS` | /users/1 |
        | `OPTIONS` | /users/1 | allow_redirects=false |
        """
        if timeout is None:
            connect_timeout = self.timeout
        else:
            connect_timeout = timeout
        Keywords.options(self, endpoint, connect_timeout, allow_redirects, validate, headers)

    @keyword
    def get(self, endpoint, query=None, timeout=None, allow_redirects=None,
            validate=True, headers=None):
        """*Sends a GET request to the endpoint.*

        The endpoint is joined with the URL given on library init (if any).
        If endpoint starts with ``http://`` or ``https://``, it is assumed
        an URL outside the tested API (which may affect logging).

        *Options*

        ``query``: Request query parameters as a JSON object or a dictionary.
        Alternatively, query parameters can be given as part of endpoint as well.

        ``timeout``: A number of seconds to wait for the response before failing the keyword. If it is not given,
        the default timeout is used instead with the timeout argument when importing the library.

        ``allow_redirects``: If false, do not follow any redirects.

        ``validate``: If false, skips any request and response validations set
        by expectation keywords and a spec given on library init.

        ``headers``: Headers as a JSON object to add or override for the request.

        *Examples*

        | `GET` | /users/1 |
        | `GET` | /users | timeout=2.5 |
        | `GET` | /users?_limit=2 |
        | `GET` | /users | _limit=2 |
        | `GET` | /users | { "_limit": "2" } |
        | `GET` | https://jsonplaceholder.typicode.com/users | headers={ "Authentication": "" } |
        """
        if timeout is None:
            connect_timeout = self.timeout
        else:
            connect_timeout = timeout
        Keywords.get(self, endpoint, query, connect_timeout, allow_redirects, validate, headers)

    @keyword
    def post(self, endpoint, body=None, timeout=None, allow_redirects=None,
             validate=True, headers=None):
        """*Sends a POST request to the endpoint.*

        The endpoint is joined with the URL given on library init (if any).
        If endpoint starts with ``http://`` or ``https://``, it is assumed
        an URL outside the tested API (which may affect logging).

        *Options*

        ``body``: Request body parameters as a JSON object, file or a dictionary.

        ``timeout``: A number of seconds to wait for the response before failing the keyword. If it is not given,
        the default timeout is used instead with the timeout argument when importing the library.

        ``allow_redirects``: If false, do not follow any redirects.

        ``validate``: If false, skips any request and response validations set
        by expectation keywords and a spec given on library init.

        ``headers``: Headers as a JSON object to add or override for the request.

        *Examples*

        | `POST` | /users | { "id": 11, "name": "Gil Alexander" } |
        | `POST` | /users | ${CURDIR}/new_user.json |
        """
        if timeout is None:
            connect_timeout = self.timeout
        else:
            connect_timeout = timeout
        Keywords.post(self, endpoint, body, connect_timeout, allow_redirects, validate, headers)

    @keyword
    def put(self, endpoint, body=None, timeout=None, allow_redirects=None,
            validate=True, headers=None):
        """*Sends a PUT request to the endpoint.*

        The endpoint is joined with the URL given on library init (if any).
        If endpoint starts with ``http://`` or ``https://``, it is assumed
        an URL outside the tested API (which may affect logging).

        *Options*

        ``body``: Request body parameters as a JSON object, file or a dictionary.

        ``timeout``: A number of seconds to wait for the response before failing the keyword. If it is not given,
        the default timeout is used instead with the timeout argument when importing the library.

        ``allow_redirects``: If false, do not follow any redirects.

        ``validate``: If false, skips any request and response validations set
        by expectation keywords and a spec given on library init.

        ``headers``: Headers as a JSON object to add or override for the request.

        *Examples*

        | `PUT` | /users/2 | { "name": "Julie Langford", "username": "jlangfor" } |
        | `PUT` | /users/2 | ${dict} |
        """
        if timeout is None:
            connect_timeout = self.timeout
        else:
            connect_timeout = timeout
        Keywords.put(self, endpoint, body, connect_timeout, allow_redirects, validate, headers)

    @keyword
    def patch(self, endpoint, body=None, timeout=None, allow_redirects=None,
              validate=True, headers=None):
        """*Sends a PATCH request to the endpoint.*

        The endpoint is joined with the URL given on library init (if any).
        If endpoint starts with ``http://`` or ``https://``, it is assumed
        an URL outside the tested API (which may affect logging).

        *Options*

        ``body``: Request body parameters as a JSON object, file or a dictionary.

        ``timeout``: A number of seconds to wait for the response before failing the keyword. If it is not given,
        the default timeout is used instead with the timeout argument when importing the library.

        ``allow_redirects``: If false, do not follow any redirects.

        ``validate``: If false, skips any request and response validations set
        by expectation keywords and a spec given on library init.

        ``headers``: Headers as a JSON object to add or override for the request.

        *Examples*

        | `PATCH` | /users/4 | { "name": "Clementine Bauch" } |
        | `PATCH` | /users/4 | ${dict} |
        """
        if timeout is None:
            connect_timeout = self.timeout
        else:
            connect_timeout = timeout
        Keywords.patch(self, endpoint, body, connect_timeout, allow_redirects, validate, headers)

    @keyword
    def delete(self, endpoint, timeout=None, allow_redirects=None, validate=True, headers=None):
        """*Sends a DELETE request to the endpoint.*

        The endpoint is joined with the URL given on library init (if any).
        If endpoint starts with ``http://`` or ``https://``, it is assumed
        an URL outside the tested API (which may affect logging).

        *Options*

        ``timeout``: A number of seconds to wait for the response before failing the keyword. If it is not given,
        the default timeout is used instead with the timeout argument when importing the library.

        ``allow_redirects``: If false, do not follow any redirects.

        ``validate``: If false, skips any request and response validations set
        by expectation keywords and a spec given on library init.

        ``headers``: Headers as a JSON object to add or override for the request.

        *Examples*

        | `DELETE` | /users/6 |
        | `DELETE` | http://localhost:8273/state | validate=false |
        """
        if timeout is None:
            connect_timeout = self.timeout
        else:
            connect_timeout = timeout
        Keywords.delete(self, endpoint, connect_timeout, allow_redirects, validate, headers)

    @keyword(name="Verify Rest Response Body")
    def verify_rest_response_body(self, expect, ignores=None, nonignores=None, check_key=False, check_datatype=False,
                            check_value=True):
        """
        Verify an actual result against an expected result.

        Custom from verify_response_body without checking key (check_key=False) and datatype (check_datatype=False). This keyword is used if Expect
        ...    Response Body keyword is used to validate schema.
        
        """
        actual = self.get_response_body()
        diffs = get_dict_diffs(actual, expect, ignores, nonignores, check_key, check_datatype, check_value)
        if diffs:
            raise AssertionError(print_friendly_message(diffs))

    @keyword(name="Verify Rest Response Status")
    def verify_rest_response_status(self, response_status):
        """
        Verify Rest Response Status
        """
        self.integer('response status', response_status)
