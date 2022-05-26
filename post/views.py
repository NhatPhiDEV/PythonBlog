from django.shortcuts import render

# Create your views here.
from .models import Post
from .serializers import PostSerializer
from rest_framework import generics

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('created')
    serializer_class = PostSerializer
