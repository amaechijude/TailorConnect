from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(data=self.context.get('request'), email=email, password=password)
            if user is None:
                raise serializers.ValidationError(_("Invalid Credentials"))
        else:
            raise serializers.ValidationError(_("provide email and/or password"))
        
        data['user'] = user
        return data

