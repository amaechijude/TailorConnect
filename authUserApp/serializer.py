from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),email=email, password=password)
            if user is None:
                raise serializers.ValidationError("Invalid Credentials")
        else:
            raise serializers.ValidationErrror("Email and/or passorwd missing")
        data['user'] = user
        return user
