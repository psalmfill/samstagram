from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


def scramble_uploaded_filename(instance, filename):
    extension = filename.split(".")[-1]
    return "media/{}.{}".format(uuid.uuid4(), extension)


class Image(models.Model):
    caption = models.CharField(max_length=255)
    file = models.ImageField(
        max_length=255, upload_to=scramble_uploaded_filename)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def comment_count(self):
        return self.comments.count()


class Comment(models.Model):
    content = models.CharField(max_length=255)
    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True)


class Like(models.Model):
    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower')
    follow = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follow")
