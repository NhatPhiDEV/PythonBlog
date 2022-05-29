from datetime import timedelta, datetime

# Create your views here.
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.pagination import PageNumberPagination
from apps.models import ActionEmoji, Comment, Post, PostView, Rating
from post.permissions import IsOwnerOrReadOnly

from .serializers import ActionSerializer, CommentSerializer, PostSerializer, PostViewSerializer, RatingSerializer
from rest_framework import generics, permissions
# Xử lý trường hợp người dùng cùng lúc chọn vào 1 blog
from django.db.models import F

class PostSearchPagination(PageNumberPagination):
    page_size = 10

class PostList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    pagination_class = PostSearchPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Post.objects.all().order_by('created_at')

class PostUpdate(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    
class PostDestroy(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# class PostUpdateDelete(generics.UpdateDestroyAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

# Update (Detail + Comment using ViewSet)
class PostDetail(viewsets.ViewSet,generics.RetrieveAPIView):
    queryset = Post.objects.filter(is_active = True)
    serializer_class = PostSerializer

    # permissions
    def get_permissions(self):
        if self.action in ['add_comment','take_action','rate']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    # Tạo mới comment
    @action(methods=['post'],detail=True,url_path='add-comment')
    def add_comment(self,request,pk):
        if content := request.data.get('content'):
            comment = Comment.objects.create(content=content
                                    ,post = self.get_object()
                                    ,creator = request.user)
            
            return Response(CommentSerializer(comment).data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    # Emoji
    # LIKE TYPE = 0, HAHA TYPE = 1, HEART TYPE = 2
    @action(methods=['post'],detail=True,url_path='like')
    def take_action(self, request,pk):
        try: 
            action_type = int(request.data['type'])
        except IndexError|ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            action = ActionEmoji.objects.create(type = action_type,creator = request.user,post = self.get_object())
            return Response(ActionSerializer(action).data,status=status.HTTP_200_OK)   
     # Rating
    @action(methods=['post'],detail=True,url_path='rating')
    def rate(self, request,pk):
        try: 
            rating = int(request.data['rating'])
        except IndexError|ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST) 
        else:
            rating = Rating.objects.create(rate = rating,creator = request.user,post = self.get_object())
            return Response(RatingSerializer(rating).data,status=status.HTTP_200_OK) 
    # View bài viết  
    @action(methods=['get'],detail=True,url_path='post_view')
    def count_view(self,request,pk):
        view, created = PostView.objects.get_or_create(post=self.get_object())
        view.views = F('views') + 1
        view.save()

        view.refresh_from_db()

        return Response(PostViewSerializer(view).data, status=status.HTTP_200_OK)

# Delete and Update Comment
class CommentViewSet(viewsets.ViewSet,generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    def destroy(self, request, *args, **kwargs):
        if request.user == self.get_object().creator:
            return super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)
    def partial_update(self, request, *args, **kwargs):
        if request.user == self.get_object().creator:
            return super().destroy(request, *args, **kwargs)
        return super().partial_update(request, *args, **kwargs)

class PostFilterByDate(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    pagination_class = PostSearchPagination

    def get_queryset(self):
        params = self.kwargs['date']
        print(params)
        start_date = datetime.strptime(params, '%Y-%m-%d')
        end_date = start_date + timedelta(days=1)
        return Post.objects.filter(created_at__range=(str(start_date), str(end_date)))

class PostCreatedByUser(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    pagination_class = PostSearchPagination

    def get_queryset(self):
        params = self.kwargs['pk']  
        return Post.objects.filter(user=params)

