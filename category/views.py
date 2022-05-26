import random

from rest_framework import generics

from .models import Category
from .serializers import CategorySerializer, NewCategorySerializer


# Create your views here.


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRandom(generics.ListAPIView):
    queryset = queryset = Category.objects.all().order_by('?')[:3]
    serializer_class = NewCategorySerializer
    
