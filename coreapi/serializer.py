from rest_framework import serializers
from coreapp.models import *


class DesignerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designer
        exclude = ['user', 'is_verified', 'joined_on']


class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style
        # fields = ('title', 'description', 'category', 'images', 'can_request')
        exclude = [ ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('text_content')

