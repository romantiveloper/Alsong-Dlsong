class CustomCsrfMiddleware(CsrfViewMiddleware):
    def _get_token(self, request):
        # user makes request to our API from Angular run on IP - add this IP to trusted origins
        if not request.META.get("HTTP_ORIGIN") in settings.CSRF_TRUSTED_ORIGINS:
            raise PermissionDenied("CSRF Failed: Origin not found in trusted origins")
        return super()._get_token(request)

