from django.urls import path

from . import views

urlpatterns = [
    path('', views.FeedView.as_view(), name='feed'),
    path('dream/new/', views.DreamCreateView.as_view(), name='dream_create'),
    path('dream/<int:pk>/', views.DreamDetailView.as_view(), name='dream_detail'),
    path('dream/<int:pk>/edit/', views.DreamUpdateView.as_view(), name='dream_update'),
    path('dream/<int:pk>/delete/', views.DreamDeleteView.as_view(), name='dream_delete'),
]
