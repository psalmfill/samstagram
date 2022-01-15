
from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers
from . import views
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'images', views.ImageViewSet)


urlpatterns = [
    path('', include(router.urls)),
    url(r'images/(?P<pk>\d+)/toggle-like/$',
        view=views.ImageViewSet.as_view({'post': 'like'})),

    url(r'images/(?P<pk>\d+)/comment/$',
        view=views.ImageViewSet.as_view({'post': 'comments'})),
    url(r'images/(?P<pk>\d+)/comment/(?P<id>\d+)/$',
        view=views.ImageViewSet.as_view({'delete': 'delete_comment'})),
    url(r'users/(?P<pk>\d+)/follow/$',
        view=views.UserViewSet.as_view({'post': 'follow'})),
    url(r'users/(?P<pk>\d+)/unfollow/$',
        view=views.UserViewSet.as_view({'post': 'unfollow'})),
    url(r'followers/$',
        view=views.UserViewSet.as_view({'get': 'followers'})),
    url(r'following/$',
        view=views.UserViewSet.as_view({'get': 'following'})),

    # url(r'posts/(?P<pk>\d+)/comments/(?P<comment>\d+)/$',
    #     view=views.PostViewSet.as_view({'delete': 'remove_comment'}))
]
