from post.serializers import PostSerializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from django.utils.translation import gettext_lazy as _

from .models import Category
from post.models import Post


class CategorySerializer(serializers.ModelSerializer):
    category_post = PostSerializer(many=True, read_only=True)  # get all post object

    class Meta:
        model = Category
        fields = ['id', 'name', 'category_post']
       

class NewCategorySerializer(serializers.ModelSerializer):
    # result_set = Post.objects.all()[:3]
    category_post = SerializerMethodField('get_limited_number_of_whatever')  # get all post object

    class Meta:
        model = Category
        fields = ['id', 'name', 'category_post']

    def get_limited_number_of_whatever(self, obj):
        query = Post.objects.all().filter(cate=obj.id)[:4]
        serializer = PostSerializer(query, many=True)
        return serializer.data
