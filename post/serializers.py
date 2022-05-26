from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'image', 'title', 'content', 'like', 'created', 'cate']
        read_only_fields = ['like']
        extra_kwargs = {
            'cate': {'write_only': True},
        }
