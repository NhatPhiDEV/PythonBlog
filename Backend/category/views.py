from rest_framework import generics, permissions

from apps.models import Category

from .serializers import CategorySerializer, NewCategorySerializer
# Create your views here.
from post.permissions import IsOwnerOrReadOnly


class CategoryList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryCreate(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,permissions.IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,permissions.IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRandom(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = queryset = Category.objects.all().order_by('?')[:3]
    serializer_class = NewCategorySerializer
    

    
