from django.urls import path

from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from post.views import PostListView, PostStatusUpdateView, LikedUserListView

router = DefaultRouter()
router.register(r'post-list', PostListView, basename='post-list')
router.register(r'update-status', PostStatusUpdateView, basename='update-status')
router.register(r'liked-users/(?P<id>\d+)', LikedUserListView, basename='liked-users')


urlpatterns = [
    path('login/', views.obtain_auth_token),
]

urlpatterns += router.urls

