from email.mime import image
from django.shortcuts import render
from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.serializers import Serializer
from . import serializers
from . import models
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django.shortcuts import get_object_or_404

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()

    @action(methods=['POST'], detail=False)
    def follow(self, request, pk):
        user_to_follow = get_object_or_404(self.queryset, pk=pk)
        if request.user == user_to_follow:
            return Response(data={'message': 'You cannot follow self.'}, status=412)
        follow = models.Follow.objects.filter(
            user=request.user, follow=pk).first()
        if(follow):
            return Response(data={'message': 'Already Following User'}, status=412)
        follow = models.Follow.objects.create(
            user=request.user, follow=user_to_follow)
        if not follow:
            return Response(data={'message': 'Could not complete request.'}, status=412)
        return Response(data={'message': 'You are now following {}.'.format(user_to_follow.username)})

    @action(methods=['POST'], detail=False)
    def unfollow(self, request, pk):
        user_to_unfollow = get_object_or_404(self.queryset, pk=pk)
        follow = models.Follow.objects.filter(
            user=request.user, follow=pk).first()
        if not follow:
            return Response(data={'message': 'You are not following {}'.format(user_to_unfollow.username)})
        follow.delete()
        return Response(data={'message': 'You unfollowed {}.'.format(user_to_unfollow.username)})

    def get_serializer_class(self):
        if self.action.lower() in ['follow', 'unfollow']:
            return serializers.EmptySerializer
        return serializers.UserSerializer

    @action(methods=['GET'], detail=False)
    def followers(self, request):
        followers = self.queryset.filter(pk__in=models.Follow.objects.filter(
            follow=request.user).values_list('user', flat=True))
        serializer = self.get_serializer_class()(
            followers, many=True, context={'request': request})
        return Response(data=serializer.data)

    @action(methods=['GET'], detail=False)
    def following(self, request):
        followers = self.queryset.filter(pk__in=models.Follow.objects.filter(
            user=request.user).values_list('follow', flat=True))
        serializer = self.get_serializer_class()(
            followers, many=True, context={'request': request})
        return Response(data=serializer.data)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = models.Image.objects.all()

    def create(self, request):
        data = request.data
        data['user_id'] = request.user.id
        serializer = self.serializer_class(
            data=data, context={'request': request})
        # check all fields is valid before attempting to save
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False)
    def like(self, request, pk):
        like = models.Like.objects.filter(image=pk, user=request.user).first()

        if(like):
            like.delete()
        else:
            like = models.Like.objects.create(
                image=models.Image.objects.get(pk=pk), user=request.user)

        return Response(data={'message': 'success'}, status=200)

    @action(methods=['POST'], detail=False)
    def comments(self, request, pk):
        # create a comment
        new_comment = models.Comment.objects.create(
            content=request.data['content'],
            user=request.user,
            image=get_object_or_404(self.queryset, pk=pk)
        )
        serializer = serializers.CommentSerializer(
            new_comment, context={'request': request})
        return Response(data=serializer.data)

    @action(methods=['DELETE'], detail=False)
    def delete_comment(self, request, pk, id):
        comment = get_object_or_404(
            models.Comment.objects.filter(user=request.user), pk=id)
        if comment.delete():
            return Response(data={'message': 'comment deleted'})
        return Response(data={'message': 'fail deleting comment.'}, status=412)

    def get_serializer_class(self):
        if self.action.lower() == 'like':
            return serializers.EmptySerializer
        if self.action.lower() == 'comments':
            return serializers.CommentSerializer
        return serializers.ImageSerializer
