from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers, models

# Create your views here.

class UserRegisterView(generics.GenericAPIView):
    serializer_class = serializers.SignUpSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                user = models.User.objects.get(phone_number=serializer.data['phone_number'])
                token = RefreshToken.for_user(user)
                return Response({
                    'message': 'User created successfully',
                    'refresh': str(token),
                    'access': str(token.access_token),
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
class UserLoginView(generics.GenericAPIView):
    serializer_class = serializers.SignInSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = authenticate(
                phone_number=serializer.validated_data['phone_number'],
                password=serializer.validated_data['password']
            )
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'User logged in successfully',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)