# blog_app/serializers.py

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Blog, Comment


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.filter(username=validated_data.get("username")).first()
        if user is None:
            user = User.objects.create_user(**validated_data)
            return user

    class Meta:
        model = User
        fields = ("username", "password")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class BlogSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = "__all__"
