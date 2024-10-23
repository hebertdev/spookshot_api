from rest_framework import serializers

#serializers
from users.serializers.users import UserModelSerializer

# models
from posts.models import Post, Media, Comment


class PostModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)
    media = serializers.SerializerMethodField('get_media')
    comments = serializers.SerializerMethodField('get_comments')
    is_like = serializers.SerializerMethodField('verify_like_user')

    def verify_like_user(self, forecast):
        if self.context:
            user = self.context['request'].user
            if not user.is_anonymous:
                return forecast.likes.filter(pk=self.context['request'].user.id).exists()
            else:
                return False
        else:
            return False

    def get_media(self, post):
        media = Media.objects.filter(post=post)  # Cambié 'posts' por 'post'
        return MediaModelSerializer(media, many=True, context=self.context).data
    
    def get_comments(self, post):
        comments = Comment.objects.filter(post=post).order_by('-created')
        return CommentModelSerializer(comments, many=True, context=self.context).data

    class Meta:
        model = Post
        fields = "__all__"


class MediaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = "__all__"


class CommentModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = "__all__"
