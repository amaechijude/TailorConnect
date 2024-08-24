from rest_framework import serializers
from .models import *


class DesignerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designer
        exclude = ['user', 'is_verified', 'joined_on']

