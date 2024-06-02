from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, UserSerializer2


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    user = request.user
    Token.objects.get(user=user).delete()
    response = {
        "success": True,
        "message": "Successfully logged out"
    }
    return Response(response, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="POST",
    operation_description="Create an object",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Description of field1'),
            'password1': openapi.Schema(type=openapi.TYPE_INTEGER, description='Description of field2'),
            'password2': openapi.Schema(type=openapi.TYPE_INTEGER, description='Description of field2'),
        },
        required=['username', 'password1', 'password2'],
        example={
            'username': 'admin',
            'password1': 'password1',
            'password2': 'password2'
        }
    ),
    responses={201: "Created", 400: "Bad Request"},
)
@api_view(["POST"])
def register_view(request):
    data = request.data
    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_profile_api_view(request):
    user = request.user
    serializer = UserSerializer2(user)
    return Response(serializer.data, status=status.HTTP_200_OK)