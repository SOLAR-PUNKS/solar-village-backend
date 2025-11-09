"""
View to serve the WebAuthn test page.
"""
from django.http import FileResponse, Http404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET
import os


@require_GET
@ensure_csrf_cookie
def webauthn_test_page(request):
    """
    Serve the WebAuthn test HTML page.
    """
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    file_path = os.path.join(static_dir, 'webauthn-test.html')
    
    if not os.path.exists(file_path):
        raise Http404("Test page not found")
    
    return FileResponse(open(file_path, 'rb'), content_type='text/html')

