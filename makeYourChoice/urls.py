"""
URL configuration for makeYourChoice project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from surveys import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ViewSurveys.as_view(), name='index'),
    path('createSurvey/', views.CreateSurvey.as_view(), name='createSurvey'),
    path('deleteSurvey/<int:pk>/', views.DeleteSurvey.as_view(), name='deleteSurvey'),
    path('viewSurvey/<int:pk>/', views.ViewSurvey.as_view(), name='viewSurvey'),
    path('addQuestion/<int:pk>/', views.AddQuestion.as_view(), name='addQuestion'),
    path('deleteQuestion/<int:pk>/', views.DeleteQuestion.as_view(), name='deleteQuestion'),
    path('addChoice/<int:pk>/', views.AddChoice.as_view(), name='addChoice'),
    path('deleteChoice/<int:pk>/', views.DeleteChoice.as_view(), name='deleteChoice'),
    path('takeSurvey/<int:pk>/', views.TakeSurvey.as_view(), name='takeSurvey'),
    path('viewResponses/<int:pk>/', views.ViewResponses.as_view(), name='viewResponses'),
    path('users/', include('django.contrib.auth.urls')),
    # previous line allows to use django's built-in login and logout views
    path('users/', include('users.urls')),
    path('createCategory/', views.CreateCategory.as_view(), name='createCategory'),
    path('deleteCategory/<int:pk>/', views.DeleteCategory.as_view(), name='deleteCategory'),
    path('editCategory/<int:pk>/', views.EditCategory.as_view(), name='editCategory'),
    path('manageCategories/', views.ManageCategories.as_view(), name='manageCategories'),
    # make path to call subscribe_to_category function
    path('subscribeToCategory/<int:pk>/', views.subscribe_to_category, name='subscribeToCategory'),
    path('unsubscribeFromCategory/<int:pk>/', views.unsubscribe_from_category, name='unsubscribeFromCategory'),
    path('manageSurveys/', views.ManageSurveys.as_view(), name='manageSurveys'),
    path('editSurvey/<int:pk>/', views.EditSurvey.as_view(), name='editSurvey'),
    path('deleteResponse/<int:pk>/', views.DeleteResponse.as_view(), name='deleteResponse'),
    path('instructions/', views.Instructions.as_view(), name='instructions'),
    path('markReady/<int:pk>/', views.mark_ready, name='markReady'),
    path('markNotReady/<int:pk>/', views.mark_not_ready, name='markNotReady'),
]
