__all__ = [
    'SetRemoteAddrFromForwardedFor',
]

class SetRemoteAddrFromForwardedFor(object):
    """
    Middleware that sets REMOTE_ADDR based on HTTP_X_FORWARDED_FOR, if the
    latter is set. This is useful if you're sitting behind a reverse proxy that
    causes each request's REMOTE_ADDR to be set to 127.0.0.1.

    Note that this does NOT validate HTTP_X_FORWARDED_FOR. If you're not behind
    a reverse proxy that sets HTTP_X_FORWARDED_FOR automatically, do not use
    this middleware. Anybody can spoof the value of HTTP_X_FORWARDED_FOR, and
    because this sets REMOTE_ADDR based on HTTP_X_FORWARDED_FOR, that means
    anybody can "fake" their IP address. Only use this when you can absolutely
    trust the value of HTTP_X_FORWARDED_FOR.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            real_ip = request.META['HTTP_X_FORWARDED_FOR']
            # HTTP_X_FORWARDED_FOR can be a comma-separated list of IPs. The
            # client's IP will be the first one.
            real_ip = real_ip.split(",")[0].strip()
            request.META['REMOTE_ADDR'] = real_ip
        except KeyError:
            pass
        return self.get_response(request)
