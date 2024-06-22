from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'message': 'Login successful'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful'}, status=200)


@api_view(['GET'])
def check_authentication(request):
    if request.user.is_authenticated:
        return JsonResponse(
            {
                'isAuthenticated': True,
                'username': request.user.username,
                'id': request.user.id
            },
            status=200
        )
    else:
        return JsonResponse({'isAuthenticated': False}, status=200)
