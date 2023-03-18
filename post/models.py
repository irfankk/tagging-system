from django.db import models
from django.contrib.auth.models import User


class Tags(models.Model):
    tag = models.CharField(max_length=30)
    wight = models.IntegerField(default=0)

    def __str__(self):
        return self.tag


class Post(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    tags = models.ManyToManyField(Tags)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Images(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='image_filename', verbose_name='Image')


class Status(models.Model):
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_status')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='status')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.like:
            self.dislike = False
        if self.dislike:
            self.like = False
        super(Status, self).save(*args, **kwargs)








