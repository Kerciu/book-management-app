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

        return super().validate(attrs)
    
    def create(self, validated_data):
        return super().create(validated_data)
