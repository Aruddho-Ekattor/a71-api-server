from rest_framework import serializers
from . import models


class EducationSerializer(serializers.ModelSerializer):
    from_date = serializers.DateField(format="%Y-%m-%d")
    to_date = serializers.DateField(format="%Y-%m-%d", required=False, allow_null=True)
    class Meta:
        model = models.Education
        fields = [
            'id',
            'institution',
            'major',
            'from_date',
            'to_date',
            'current',
            'description',
        ]


class ExperienceSerializer(serializers.ModelSerializer):
    from_date = serializers.DateField(format="%Y-%m-%d")
    to_date = serializers.DateField(format="%Y-%m-%d", required=False, allow_null=True)
    class Meta:
        model = models.Experience
        fields = [
            'id',
            'title',
            'company',
            'from_date',
            'to_date',
            'current',
            'description',
        ]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = [
            'id',
            'address',
            'skills',
            'profile_picture',
            'cover_photo',
            'about',
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    education = EducationSerializer(many=True)
    experience = ExperienceSerializer(many=True)

    class Meta:
        model = models.User
        fields = [
            'id',
            'email',
            'phone_number',
            'full_name',
            'user_type',
            'profile',
            'education',
            'experience',
        ]

