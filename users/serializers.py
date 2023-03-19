from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
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
        user = User.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            phone_number=validated_data['phone_number'],
            user_type=validated_data['user_type'],
            password=validated_data['password'],
        )
        return user
    

class SignInSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13, required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = User.objects.filter(phone_number=data['phone_number']).first()
        if user is None:
            raise serializers.ValidationError("User with this phone number does not exist")
        if not user.check_password(data['password']):
            raise serializers.ValidationError("Incorrect password")
        return data