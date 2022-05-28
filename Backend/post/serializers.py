from rest_framework import serializers

from apps.models import ActionEmoji, Comment, Post, PostView, Rating


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.show')

    class Meta:
        model = Post
        fields = ['id', 'image', 'title', 'content', 'created_at', 'category', 'user']
        extra_kwargs = {
            'category': {'write_only': True},
        }

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content','post','creator','created_at']      

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionEmoji
        fields = ['id','type','created_at']
        
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id','type','created_at']
class PostViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostView
        fields  = ['id','views','post']