from . import models
from rest_framework import serializers

class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = [
            'email',
            'full_name',
            'phone_number',
            'user_type',
            'password',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = models.User.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            phone_number=validated_data['phone_number'],
            user_type=validated_data['user_type'],
            password=validated_data['password']
        )
        return user
    

class SignInSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.User
        fields = [
            'phone_number',
            'password',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }