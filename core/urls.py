from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('request/raise/', views.raise_request, name='raise_request'),
    path('request/<int:pk>/respond/', views.respond_request, name='respond_request'),
    path('volunteers/', views.volunteer_list, name='volunteer_list'),
    path('volunteers/<int:pk>/', views.volunteer_detail, name='volunteer_detail'),
]