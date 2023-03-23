from . import models, serializers
from rest_framework.response import Response
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


class ProfileView(generics.GenericAPIView):
    serializer_class = serializers.UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user = models.User.objects.get(pk=request.user.id)
            serializer = serializers.UserProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.Profile.DoesNotExist:
            return Response({'error': 'Profile does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = serializers.UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)