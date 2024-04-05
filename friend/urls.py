from django.urls import path, re_path
from friend import views

urlpatterns = [
    path(
        'list/', views.ListFriendsAPIView.as_view(),
        name='list-friend-requests'
    ),
    path(
        'pending-list/', views.ListPendingFriendsAPIView.as_view(),
        name='pending-list-friend-requests'
    ),
    re_path(
        r'^request/(?P<response_text>\w+)/$', views.RequestAPIView.as_view(),
        name="send-accept-reject-requests"
    ),
]
