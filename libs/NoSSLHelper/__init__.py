import ssl
__version__ = '1'
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


class NoSSLHelper:
    """
    Helper library for create unveifield SSL context (No SSL) and HTTPs. Supported UI (Web Application) testing.
    """

    ROBOT_LIBRARY_VERSION = __version__

    def run(self):
        """
        Checked method for unverified context.
        """
        pass
