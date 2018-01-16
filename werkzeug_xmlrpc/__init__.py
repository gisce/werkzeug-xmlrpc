from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import BadRequest, InternalServerError

__version__ = '0.1.0'


class WSGIXMLRPCApplication(object):
    """Application to handle requests to the XMLRPC service"""

    def __init__(self, instance=None, methods=()):
        """Create windmill xmlrpc dispatcher"""
        try:
            self.dispatcher = SimpleXMLRPCDispatcher(
                allow_none=True, encoding=None
            )
        except TypeError:
            # python 2.4
            self.dispatcher = SimpleXMLRPCDispatcher()

        if instance is not None:
            self.dispatcher.register_instance(instance)

        for method in methods:
            self.dispatcher.register_function(method)

        self.dispatcher.register_introspection_functions()

    @Request.application
    def handler(self, request):
        if request.method == 'POST':
            return self.handle_POST(request)
        else:
            return BadRequest()

    def handle_POST(self, request):
        """Handles the HTTP POST request.

        Attempts to interpret all HTTP POST requests as XML-RPC calls,
        which are forwarded to the server's _dispatch method for handling.

        Most code taken from SimpleXMLRPCServer with modifications for wsgi and
        my custom dispatcher.
        """

        try:
            # Read the data from the request
            data = request.get_data()

            # In previous versions of SimpleXMLRPCServer, _dispatch
            # could be overridden in this class, instead of in
            # SimpleXMLRPCDispatcher. To maintain backwards compatibility,
            # check to see if a subclass implements _dispatch and
            # using that method if present.
            response = self.dispatcher._marshaled_dispatch(
                data, getattr(self.dispatcher, '_dispatch', None)
            )
            response += '\n'
        except:  # This should only happen if the module is buggy
            # internal error, report as HTTP server error
            return InternalServerError()
        else:
            # got a valid XML RPC response
            return Response(response, mimetype='text/xml')

    def __call__(self, environ, start_response):
        return self.handler(environ, start_response)
