class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # This is called before the next middleware is called
        request.META['ANOTHER_KEY'] = 'Joshua was here'
        response = self.get_response(request)
        # This is called after the view is called ie on the return journey
        assert False
        return response


# Can also create a middleware as a function
def my_middleware(get_response):
    # Configuration and initialization
    def middleware(request):
        # This is called before the next middle ware is called
        request.META['CUSTOM_KEY'] = 'Joshua is here'
        response = get_response(request)
        # Thi is called after the view is called i.e on the return journey
        assert False
        return response
    return middleware