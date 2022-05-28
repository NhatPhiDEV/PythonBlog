from django.urls import path,include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('detail',views.PostDetail,'detail')
router.register('comments',views.CommentViewSet,'comments')

urlpatterns = [
    path('actions/',include(router.urls)),
    path('', views.PostList.as_view()),
    path('update/<int:pk>', views.PostUpdate.as_view()),
    path('delete/<int:pk>', views.PostDestroy.as_view()),
    # path('<int:pk>/', views.PostDetail.as_view()),
    path('filter/<str:date>/', views.PostFilterByDate.as_view()),
    path('<int:pk>/user/', views.PostCreatedByUser.as_view()),
]
