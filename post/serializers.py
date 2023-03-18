from django.contrib.auth.models import User

from rest_framework import serializers

from post.models import Post, Images, Status


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ('image', )


class PostSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    current_status = serializers.SerializerMethodField()

    def get_images(self, obj):
        return [ImageSerializer(s).data for s in obj.images.all()]

    def get_like_count(self, obj):
        return obj.status.filter(like=True).count()

    def get_dislike_count(self, obj):
        return obj.status.filter(dislike=True).count()

    def get_current_status(self, obj):
        request = self.context.get('request', None)
        data = obj.status.filter(user=request.user)
        if not data:
            return None
        elif not data[0].like and not data[0].dislike:
            return None
        result = 'like' if data[0].like else 'dislike'
        return result

    class Meta:
        model = Post
        fields = ('title', 'description', 'tags', 'images', 'like_count', 'dislike_count',
                  'current_status', 'created_at')
        depth = 1


class StatusSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Status
        fields = ('like', 'dislike', 'post', 'user')

    def validate(self, data):
        if data.get('like', False) and data.get('dislike', False):
            raise serializers.ValidationError("Can't add like and dislike same post")
        return data


class UserListSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_email(self, obj):
        return obj.user.email

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Status
        fields = ('first_name', 'last_name', 'email', 'username')
        depth = 1






