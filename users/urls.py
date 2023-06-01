from django.urls import path
from . import views

urlpatterns = [
    path('login_user', views.login_user, name='login_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('register_user', views.register_user, name='register_user'),
    path('search_user', views.search_user, name='search_user'),
    path('manage_followed_users', views.ManageFollowedUsers.as_view(), name='manage_followed_users'),
    path('follow_user/<int:pk>', views.follow_user, name='follow_user'),
    path('unfollow_user/<int:pk>/', views.unfollow_user, name='unfollow_user'),
    path('is_following/<int:pk>/', views.is_following, name='is_following'),
    path('deleteUser', views.DeleteUser.as_view(), name='deleteUser'),
    path('delete_user/<int:pk>/', views.delete_user, name='delete_user'),
]