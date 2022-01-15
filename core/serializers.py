from django.db.models import fields
from . import models
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.models import AnonymousUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'is_staff']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = models.Comment
        fields = ['id', 'content', 'user']


class ImageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    liked = serializers.SerializerMethodField(method_name='has_like')

    class Meta:
        model = models.Image
        fields = ['id', 'caption', 'url', 'user', 'comments',
                  'like_count',  'file', 'liked']

    def has_like(self, obj):
        if isinstance(self.context['request'].user, AnonymousUser):
            return False
        return models.Like.objects.filter(image=obj, user=self.context['request'].user).first() != None


class EmptySerializer(serializers.Serializer):
    pass
