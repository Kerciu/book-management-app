from rest_framework import serializers
from .models import CustomUser

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    re_password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password', 're_password']

    def validate(self, attrs):

        password = attrs.get('password', '')
        re_password = attrs.get('re_password', '')
        if password != re_password:
            raise serializers.ValidationError("Passwords do not match")

        return attrs
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user
