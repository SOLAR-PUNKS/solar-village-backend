"""
Views for WebAuthn passkey authentication that return JWT tokens.
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django_otp import user_has_device


@api_view(['POST'])
@permission_classes([AllowAny])
def webauthn_token_view(request):
    """
    View that returns JWT tokens after successful passkey authentication.
    
    This view expects the user to be authenticated via WebAuthn before calling.
    The client should complete the WebAuthn authentication flow first using the
    django-otp-webauthn endpoints, then call this endpoint to receive JWT tokens.
    
    The user should be authenticated via the WebAuthnBackend before reaching this view.
    This typically happens after completing the authentication flow at /webauthn/login/
    """
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return Response(
            {'error': 'User must be authenticated via passkey first. Complete authentication at /webauthn/login/'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Verify user has a WebAuthn device (passkey)
    if not user_has_device(request.user):
        return Response(
            {'error': 'User does not have a registered passkey'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Generate JWT tokens
    refresh = RefreshToken.for_user(request.user)
    
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }, status=status.HTTP_200_OK)

